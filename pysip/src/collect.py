#------------------------------------------------------------------------------#
#                     Author     : Nicklas Sindlev Andersen                    #
#                     Website    : Nicklas.xyz                                 #
#                     Github     : github.com/NicklasXYZ                       #
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#
#                               Import local code                              #
#------------------------------------------------------------------------------#
from .CommandLineArgs import CommandLineArgs
from .RandomHTMLDocument import RandomHTMLDocument
from .utils import (
    str_to_bool,
    print_verbose,
)
from .color_palettes import (
    COLOR_PALETTES,
    update_color_palettes,
)
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import shutil
import json 
import os
import stat
import time
from io import StringIO
from pathlib import Path
#------------------------------------------------------------------------------#
#                           Import third party packages                        #
#------------------------------------------------------------------------------#
from lxml import etree  # pip install lxml
import jinja2           # pip install jinja2


#------------------------------------------------------------------------------#
class StaticIndexPage:
    """
    class: StaticIndexPage. This class organizes a number of functions and
    variables that are used in the process of generating a static index page.
    """


    def __init__(self, args):
        """ 
        """
        # Store the given commandline arguments
        self.args = args
        # Set the default or user-specified color palette
        self.color_palette = self.set_color_palette()

        # Set all necessary directories and file paths
        # - Current working directory:
        self.cwd = os.getcwd()
        # - The user-specified content directory:
        self.content_dir = os.path.join(self.cwd, self.args.content_dir)
        # - The directory where the python library is located/was installed to:
        origin_dir = os.path.dirname(
            os.path.dirname(__file__),
        )
        # - The directory where all static index page assets are located:
        self.assets_dir = os.path.join(origin_dir, "staticfiles")
        # - The directory where all static index page templates are located:
        self.template_dir = os.path.join(origin_dir, "base")
        print("template_dir: ", self.template_dir)

        # Check all directories, i.e. either validate, create or delete
        # directories
        self.check_directories()
        # Generate random test data to test the layout of the static index page
        # if the user specified so via the "-test_data/--test_data" commandline
        # argument
        self.generate_test_data()
        # Finally, render templates and collect all necessary data. Copy the 
        # files to the destination directory (the directory where the "pysip"
        # command was run)
        self.generate_static_index_page()


    def generate_test_data(self):
        """ 
        """
        if self.args.test_data > 0:
            # Generate "n" random HTML documents for testing purposes and place
            # them in the directory which was specified via the "-d/--content_dir"
            # commandline argument
            RandomHTMLDocument(
                args = self.args,
                n = self.args.test_data
            ).save(
                content_dir = self.content_dir,
            )


    def generate_static_index_page(self):
        """
        """
        # Copy assets to the destination directory (the directory where the
        # "pysip" command was run)
        print_verbose("INFO : Copying assets and other static files to the " + \
            "destination directory...", self.args.verbose,
        )
        self.copy_static_files()
        # Load all templates located in the "base" template directory
        jinja_templates = self.load_jinja_templates()
        # Render the templates using the user-specified color palette
        self.render_templates(
            jinja_templates,
            COLOR_PALETTES[self.args.color_palette],
        )
        # Go through the directories in the directory given via the commandline
        # argument "-d/--content_dir". Collect data from the "index.html" 
        # file which may be contained in a subdirectory
        print_verbose("INFO : Traversing directories containing HTML files...", 
            self.args.verbose,
        )
        files = self.traverse_dirs()
        print_verbose("INFO : Ordering the files...", self.args.verbose)
        files = self.order_files(files)
        destination_dir = os.path.join(self.cwd, "staticfiles")
        file = os.path.join(destination_dir, "filelist.js")
        print_verbose(f"INFO : Writing data to file {file}", self.args.verbose)
        # Create a Javascript file with .json data that contains all the 
        # collected data. Save the Javascript file in the destination 
        # directory (the directory where the "pysip" command was run)
        with open(file, "w") as file:
            file.write("var FILE_LIST = ")
            file.write(json.dumps(files, indent = 4))


    def check_directories(self):
        """ Based on the given commandline arguments either validate, 
        create or delete directories.
        """
        # Check if the user-specified "content_dir" actually exists. If test
        # data is going to be generated, then it is fine if the "content_dir"
        # directory does not exist initially. It will after test data has
        # been generated
        if not os.path.exists(self.content_dir) and self.args.test_data == 0:
            print(f"ERROR: No such directory {self.content_dir}")
            print_verbose("INFO : Terminating...", self.args.verbose)
            raise SystemExit

        # Check whether the content directory is actually a parent directory.
        # If the content directory is a parent directory and not a subdirectory,
        # then the relative paths added, in the static index page, will not be 
        # correct.
        root = Path(self.cwd)
        if not root in [p for p in Path(self.content_dir).resolve().parents]:
            print("ERROR: The content directory supplied via the commandline " + \
                "argument \"-d/--content_dir\" can not be a parent directory! " + \
                "It needs to be a subdirectory.")
            print_verbose("INFO : Terminating...", self.args.verbose)
            raise SystemExit

        # Create/re-create the required "staticfiles" output directory if it
        # is missing/already exists
        destination_dir = os.path.join(self.cwd, "staticfiles")
        if os.path.exists(destination_dir):
            print("ERROR: A directory with the name \"staticfiles\" " + \
                "already exists in the current working directory!")
            answer = str_to_bool(input("\n    → Do you want to " + \
                "overwrite the files in the current \"staticfiles\" " + \
                "directory? (yes/no):\n    → "))
            if answer == True:
                # Remove files
                shutil.rmtree(destination_dir)
                print_verbose(
                    "INFO : Removing files in directory: " + str(destination_dir),
                    self.args.verbose,
                )
            else:
                print_verbose("INFO : Terminating...", self.args.verbose)
                raise SystemExit


    def set_color_palette(self):
        """ Using a certain color palette, update one or more of the colors.
        """
        global COLOR_PALETTES
        update_color_palettes(
            name = self.args.color_palette,
            color1 = self.args.color1, # Page head color
            color2 = self.args.color2, # Page body color
            color3 = self.args.color3, # Page text color 1
            color4 = self.args.color4, # Page text color 2
        )
        return COLOR_PALETTES


    def traverse_dirs(self):
        """ Go through each directory in the given directory and look
        for HTML files with the name "index.html". Extract and save 
        metadata and the relative filepath to each of these files, 
        such that they can eventually be included in the final static
        index page.

        Args:
            None

        Returns:
            files (list(dict)): A list of dictionaries. Each dictionary
                contains the relative path and metadata of a static file
                found in a directory, in the directory given via the 
                commandline argument "-d/--content_dir"
        """
        files = []; content_dirs = os.listdir(self.content_dir)
        # Go through all directories
        for item in content_dirs:
            # Look in each directory for an "index.html" file
            file_dir = os.path.join(self.content_dir, item)
            content_files = os.listdir(file_dir)
            # If an "index.html" file is found, then extract the
            # appropriate data
            if "index.html" in content_files:
                file_metadata = {}
                index_path = os.path.join(
                    self.content_dir,
                    item,
                    "index.html"
                )
                # Use the lxml python library to parse the title and
                # data contained in the HTML metadata tags 
                with open(index_path) as f:
                    parser = etree.HTMLParser()
                    tree = etree.parse(StringIO(f.read()), parser)
                file_metadata = self.extract_html_file_data(tree)
                # Save the relative path to the "index.html" file
                file_metadata["url"] = os.path.join(
                    self.args.content_dir,
                    item,
                    "index.html",
                )
                # Save the name of the directory where the "index.html"
                # file was found
                file_metadata["dir"] = item
                # Try to extract some additional metadata saved by the
                # filesystem 
                try:
                    st = os.stat(index_path)
                except IOError:
                    print(
                        "ERROR: failed to read information " + \
                        f"about the file {index_path}!"
                    )
                else:
                    file_metadata["last_modified_formatted"] = \
                        time.asctime(time.localtime(st[stat.ST_MTIME]))
                    file_metadata["last_modified_raw"] = \
                        st[stat.ST_MTIME]
                files.append(file_metadata)
        print_verbose("INFO : All necessary data has been extracted from the " + \
            "files...", self.args.verbose,
        )
        return files

    def order_files(self, files):
        """ Order a set of files according to a certain user-specified
        criteria.

        Args:
            files (list(dict)): A list of dictionaries. Each 
                dictionary contains information about a certain
                "index.html" file.

        Returns:
            files (list(dict)): A list of dictionaries. The list
                has been ordered according to a certain criteria
                specified by the user on the commandline. 

        """
        # Order the keywords lexicographically
        for file in files:
            if not file["keywords"] == "":
                file["keywords"].sort(key = lambda x: x)
        # Order the files by date and time of when it was last
        # modified
        if self.args.order_by == "last_modified":
            files.sort(key = lambda x: x["last_modified_raw"])
        # Order the files lexicographically by author
        elif self.args.order_by == "author":
            files.sort(key = lambda x: x["author"])
        # Order the files lexicographically by title
        elif self.args.order_by == "title":
            files.sort(key = lambda x: x["name"])
        # Order the files lexicographically by the name of the
        # directories they are placed in
        elif self.args.order_by == "directory_name":
            files.sort(key = lambda x: x["dir"])
        return files


    def extract_html_file_data(self, tree):
        """ Extract metadata from a certain HTML file represented by an 
        object "tree".

        Args:
            tree (lxml.etree._ElementTree): An object representation of 
                a certain HTML file.

        Returns: A dictionary that contains the relative path and metadata
            of an "index.html" file which was found within one of the 
            directories in the directory which was specified via the 
            "-d/--content_dir" commandline argument.
        """
        file = {}
        # Get the title of the "index.html" document
        title = tree.find(".//title")
        file["name"] = title.text.strip()
        # Get all elements of the DOM that has the meta tag
        dom_elements = tree.findall(".//meta")
        for element in dom_elements:
            if "name" in element.attrib:
                # Get all the keywords listed in the "index.html" document
                if element.attrib["name"] == "keywords":
                    file["keywords"] = [
                        keyword.strip() for keyword in \
                        element.attrib["content"].split(",")
                    ]
                # Get the description of "index.html" document
                if element.attrib["name"] == "description":
                    file["description"] = element.attrib["content"].strip()
                # Get the author of "index.html" document
                if element.attrib["name"] == "author":
                    file["author"] = element.attrib["content"].strip()
        # In case no data was read, then set a default value (empty string)
        if not "keywords" in file:
            file["keywords"] = ""
        if len(file["keywords"]) == 1:
            if file["keywords"][0] == "":
                file["keywords"] = ""
        if not "description" in file:
            file["description"] = ""
        if not "author" in file:
            file["author"] = ""
        return file


    def copy_static_files(self):
        """ Copy all assets from the library directory to the destination
        directory (the directory where the "pysip" command was run).
        """
        staticfiles_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ), "staticfiles",
        )
        print_verbose(
            "INFO : Copying files to directory: " + \
            str(os.path.join(self.cwd, "staticfiles")),
            self.args.verbose,
        )
        try:
            shutil.copytree(
                staticfiles_dir,
                os.path.join(self.cwd, "staticfiles"),
            ) 
            print_verbose(
                "INFO : Files copied successfully!",
                self.args.verbose,
            ) 
        # Catch duplicate file errors 
        except shutil.SameFileError: 
            print("ERROR: Source and destination files are identical!") 
        # Catch permission errors
        except PermissionError: 
            print("ERROR: Permission denied.") 
        # For other errors 
        except Exception as e:
            print("ERROR: An error occurred while copying the files!") 
            print("ERROR: ", e)


    def load_jinja_templates(self):
        """ Load the folder containing jinja2 templates.

        Args:
            None

        Returns:
            jinja_template (jinja2.environment.Environment): A jinja2 
                object which contains the paths to all the necessary
                templates that will need to be rendered.
        """
        try:
            jinja_templates = jinja2.Environment(
                autoescape = True,
                loader = jinja2.FileSystemLoader(
                    searchpath = self.template_dir,
                ),
            )
        except KeyError as e:
            print("ERROR: Template directory not defined!")
            print("ERROR: ", e)
        return jinja_templates


    def render_template(self, jinja_templates, template_vars, 
        template_name, outfile):
        """ Given a template name and a dictionary "template_vars" of
        values, render the template.

        Args:
            jinja_template (jinja2.environment.Environment): A jinja2 
                object which contains the paths to all the necessary
                templates that will need to be rendered.
            template_vars (dict): A set of values to use when rendering
                the template.
            template_name (str): The name of the template to render.
            outfile (str): The name of the output file (rendered template).

        Returns:
            None
        """
        template = jinja_templates.select_template([template_name])
        with open(outfile, "w") as file:
            print(template.render(**template_vars), file = file)


    def render_templates(self, jinja_templates, template_vars):
        """ Given a dictionary "template_vars" of values, render the 
        different templates listed below.

        Args:
            jinja_template (jinja2.environment.Environment): A jinja2
                object which contains the paths to all the necessary
                templates that will need to be rendered.
            template_vars (dict): A set of values to use when rendering
                the template.
        
        Returns:
            None
        """
        destination_dir = os.path.join(self.cwd, "staticfiles")
        # - Render the index.css file
        self.render_template(
            jinja_templates,
            template_vars,
            # The template file to use. Should not be changed:
            "index.html.jinja",
            # Specify the correct directory to place the file in
            os.path.join(self.cwd, "index.html"), 
        )
        # - Render the index.css file
        self.render_template(
            jinja_templates,
            template_vars,
            # The template file to use. Should not be changed:
            "index.css.jinja",
            # Specify a filename and the correct directory to place
            # the file in
            os.path.join(destination_dir, "index.css"), 
        )
        # - Render the main_image.svg file
        self.render_template(
            jinja_templates,
            template_vars,
            # The template file to use. Should not be changed:
            "main_image_1.svg.jinja",
            # Specify a filename and the correct directory to place
            # the file in
            os.path.join(destination_dir, "main_image.svg"), 
        )


# Main function call...
#------------------------------------------------------------------------------#
def main():
    """ Main function call. Collect metadata from static files and save their 
    corresponding relative paths. Write out the collected data to a Javascript
    file that can later be included in a final HTML document.
    """

    # Get the given commandline arguments
    args = CommandLineArgs().args
    # Generate a static index page 
    StaticIndexPage(args)


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    Script entry point...
    """
    main()
