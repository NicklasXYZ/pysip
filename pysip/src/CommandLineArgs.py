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
    str_to_bool,
    is_integer,
    is_hex,
    print_verbose,
)
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import argparse
import re


#------------------------------------------------------------------------------#
class CommandLineArgs:
    """
    class: CommandLineArgs. A simple class that uses the "argparse" library
    from the python standard library. The class simply wraps a number of
    functions to make it easy to add optional and required commandline
    arguments.
    """


    def __init__(self, args_list = None):
        """
        """
        self.args = self.get_commandline_args(args_list)


    def get_commandline_args(self, args_list = None):
        """ Setup, parse and validate given commandline arguments.
        """
        # Create main parser
        parser = argparse.ArgumentParser(description = "")
        self.add_parser_arguments(parser)
        # Parse commandline arguments
        args = parser.parse_args(args_list)
        # Check the given commandline arguments
        self.check_args(args)
        return args


    def add_required_parser_arguments(self, parser):
        """
        """
        parser.add_argument("-d", "--content_dir",
            required = True,
            default = None,
            type = str,
            help = "Specify a path to a directory containing directories " + \
                "that each contain an \"index.html\" file.",
        )


    def add_optional_parser_arguments(self, parser):
        """
        """
        ### Options: Generation of test data for testing purposes...
        parser.add_argument("-v", "--verbose",
            required = False,
            default = False,
            type = str_to_bool,
            help = "Ex: -v True. Specify whether information about the generation of " + \
                "the static index page should be shown.",
        )

        ### Options: Generation of test data for testing purposes...
        parser.add_argument("-test_data", "--test_data",
            required = False,
            default = "0",
            type = str,
            help = "Ex: -test_data 125. Specify whether some random " + \
                "test data should be generated.",
        )

        #### Options: How the ordering of the files in the grid should be
        parser.add_argument("-order_by", "--order_by",
            required = False,
            default = "last_modified",
            type = str,
            choices = ["last_modified", "title", "author", "directory_name"],
            help = "Ex: -order_by title. Specify how the items in the grid " + \
                "(placed in the main body of the HTML document) should be " + \
                "ordered.",
        )

        ### Options: Pre-defined styling/color palette
        parser.add_argument("-color_palette", "--color_palette",
            required = False,
            default = "color_palette_4",
            type = str,
            choices = [
                "color_palette_1",
                "color_palette_2",
                "color_palette_3",
                "color_palette_4",
            ],
            help = "Ex: -color_palette dark_green. Specify a pre-defined " + \
                "color palette for the HTML document that is going to be " + \
                "generated.",
        )

        ### Options: Custom styling
        parser.add_argument("-color1", "--color1",
            required = False,
            default = None,
            type = str,
            help = "Ex: -color1 \"#717171\". Specify the background color used " + \
            "in the header and footer of the HTML document.",
        )
        parser.add_argument("-color2", "--color2",
            required = False,
            default = None,
            type = str,
            help = "Ex: -color2 \"#ffffff\". Specify the background color used " + \
            "in the body of the HTML document.",
        )
        parser.add_argument("-color3", "--color3",
            required = False,
            default = None,
            type = str,
            help = "Ex: -color3 \"#8939a8\". Specify the color of the title, " + \
                "description and the text in the footer, of the HTML " + \
                "document. A faded version of this color is also used by " + \
                "the description displayed in each item in the grid " + \
                "(placed in the main body of the HTML document).",
        )
        parser.add_argument("-color4", "--color4",
            required = False,
            default = None,
            type = str,
            help = "Ex: -color4 \"#000000\". Specify the main color of the icon " + \
                "(shown at the top of the HTML document). This color is also " + \
                "used by the title displayed in each item in the grid (placed "+ \
                "in the main body of the HTML document).",
        )


    def add_parser_arguments(self, parser):
        """ This function defines the possible commandline arguments for the main
        parser.

        Args:
            parser (argparse.ArgumentParser): A parser object, where required and
                optional commandline arguments can be defined. Eventually, when the
                python program is run, it will be possible to provide input for the
                commandline arguments defined below.

        Returns:
            None
        """
        # Add required commandline arguments:
        self.add_required_parser_arguments(parser)
        # Add optional commandline arguments:
        self.add_optional_parser_arguments(parser)


    def check_required_arguments(self, args):
        """
        """
        # if not os.path.exists(cwd):
        pass


    def check_optional_arguments(self, args):
        """
        """
        # Options: Generation of test data for testing purposes...
        # - Check whether the input is actually integer-valued
        if not is_integer(args.test_data):
                raise ValueError(f"--test_data {args.test_data}. The provided" + \
                    "value is not integer-valued!",
                )
        else:
            args.test_data = int(args.test_data)
        # Options: Custom styling
        # - Check if the custom color options are valid.
        if not args.color1 is None:
            if not is_hex(args.color1):
                raise ValueError(f"--color1 {args.color1}. The provided" + \
                    "color is not a valid hex color code!",
                )
        if not args.color2 is None:
            if not is_hex(args.color2):
                raise ValueError(f"--color1 {args.color2}. The provided" + \
                    "color is not a valid hex color code!",
                )
        if not args.color3 is None:
            if not is_hex(args.color3):
                raise ValueError(f"--color1 {args.color3}. The provided" + \
                    "color is not a valid hex color code!",
                )
        if not args.color4 is None:
            if not is_hex(args.color4):
                raise ValueError(f"--color1 {args.color4}. The provided" + \
                    "color is not a valid hex color code!",
                )


    def check_args(self, args):
        """ This function validates a subset of the given commandline arguments.

        Args:
            args (argparse.Namespace): An object which contains all the given input
                values of the previously defined commandline arguments (these
                commandline arguments are defined in the add_parser_arguments()
                function).

        Returns:
            None
        """
        print_verbose("INFO : Checking commandline arguments...", args.verbose)
        self.check_required_arguments(args)
        self.check_optional_arguments(args)
        return args
