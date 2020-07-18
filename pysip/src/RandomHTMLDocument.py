#------------------------------------------------------------------------------#
#                     Author     : Nicklas Sindlev Andersen                    #
#                     Website    : Nicklas.xyz                                 #
#                     Github     : github.com/NicklasXYZ                       #
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#
#                               Import local code                              #
#------------------------------------------------------------------------------#
from .utils import (
    print_verbose,
)
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import random
import os
#------------------------------------------------------------------------------#
#                           Import third party packages                        #
#------------------------------------------------------------------------------#
from lxml import etree  # pip install lxml
from faker import Faker # pip install faker


#------------------------------------------------------------------------------#
class RandomHTMLDocument:
    """
    class: RandomHTMLDocument. This class organizes a number of functions that
    are used for generating and organizing a number of random HTML documents.
    These randomly generated documents can then be used to test the main
    functionality of the pysip commandline tool.
    """


    def __init__(self, args, n = 1):
        """ Initialize class variables and call the main function 
        "generate_document" to generate "n" random HTML documents.

        Args:
            n (int): The number of random HTML documents to generate.
        
        Returns:
            None
        """
        self.args = args
        self.n = n
        # The variable that holds a list of string representations of
        # randomly generated HTML documents
        self.doc_strings = []
        print_verbose(
            "INFO : Generating random HTML documents...",
            self.args.verbose,
        )
        # Generate a number of random HTML documents
        for i in range(self.n):
            self.doc_strings.append(self.generate_document())


    def generate_document(self):
        """ Generate a random HTML document.
        """
        faker = Faker()
        # Start creating a HTML document...
        html = etree.Element("html")
        head = etree.Element("head")
        # Set the document title
        title = etree.Element("title")
        title.text = faker.sentence()
        head.append(title) # Add the title to the head of the document
        # Set document keywords
        keywords = ", ".join([word for word in faker.words(random.randint(0, 6))])
        keywords = etree.Element(
            "meta",
            name = "keywords",
            content = keywords,
        )
        head.append(keywords) # Add the keywords to the head of the document
        # Set document description
        description = faker.paragraph(random.randint(0, 10))
        description = etree.Element(
            "meta",
            name = "description",
            content = description,
        )
        head.append(description) # Add the description to the head of the document
        # Set document author
        author = faker.name()
        author = etree.Element(
            "meta",
            name = "author",
            content = author,
        )
        head.append(author) # Add the author to the head of the document
        # Append the head to the html document
        html.append(head)
        # Add some content to the body of the document
        body = etree.Element("body")
        center = etree.Element("center")
        h1 = etree.Element("h1")
        h1.text = title.text
        center.append(h1)
        body.append(center)
        # Append the body of the document to the HTML document
        html.append(body)
        # return a string representation of the HTML document
        return etree.tostring(html, pretty_print = True)


    def save(self, content_dir):
        """ Save the HTML documents py place them in the given "content_dir"
        directory.

        Args:
            content_dir (str) : The relative path to a directory that contains
                directories. Each directory may contain an "index.html" file.

        Returns:
            None
        """
        print_verbose(
            "INFO : Writing random HTML documents to files...",
            self.args.verbose,
        )
        for i in range(self.n):
            dir_path = content_dir + "/" + "staticpage" + str(i)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            index_file = os.path.join(dir_path, "index.html") 
            with open(index_file, "w") as file:
                file.write(self.doc_strings[i].decode("utf-8"))
