#------------------------------------------------------------------------------#
#                     Author     : Nicklas Sindlev Andersen                    #
#                     Website    : Nicklas.xyz                                 #
#                     Github     : github.com/NicklasXYZ                       #
#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import re


#------------------------------------------------------------------------------#
def str_to_bool(s):
    """ Convert a string to a boolean value.

    Args:
        s (str): A string.

    Returns:
        (bool): True if the string has boolean value True. False if the string
            has boolean value False.
    """
    s = s.strip() # Strip whitespace
    if s.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif s.lower() in ("no", "false", "f", "n", "0"):
        return False


def is_integer(s):
    """ Simply check whether or not a given input is a string or an integer

    Args:
        s (str): A string.

    Returns:
        (bool): True if the string can be cast as an int. False if the string
            can not be cast as an int (it is actually not an int).
    """
    try:
        int(s);
        return True
    except ValueError:
        return False


def is_hex(s):
    """ Check whether a string is actually a hex color code.

    Args:
        s (str): A string and possibly a hex color code.

    Returns:
        (bool): True if the input is a valid hex color code and
            False if it is not.
    """
    match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", s)
    if match:
        return True
    else:
        return False


def rgb(hex):
    """ 

    Args:
        s (str): A hex color code as a string.

    Returns:
        r (int): Red color value.
        g (int): Green color value.
        b (int): Blue color value.
    """
    r, g, b = bytes.fromhex(hex)
    return r, g, b


def hex(r, g, b):
    """

    Args:
        r (int): Red color value.
        g (int): Green color value.
        b (int): Blue color value.

    Returns:
        (str): A hex color code as a string.
    """
    return bytes((r, g, b)).hex()


def print_verbose(s, v):
    """ Just a wrapper method for the print function.

    Args:
        s (str) : A string to print to std output.
        v (bool): A boolean value that decides whether the string
            is printed or not.

    Returns:
        None
    """
    if v:
        print(s)

