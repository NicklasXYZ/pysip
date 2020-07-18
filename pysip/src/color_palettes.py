
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
    rgb,
)


#------------------------------------------------------------------------------#
#                           Global variables & methods                         #
#------------------------------------------------------------------------------#
global COLOR_PALETTES
COLOR_PALETTES = {}


def update_color_palettes(
        name, color1 = None, color2 = None, color3 = None, color4 = None,
    ):
    """ Given a color palette name and colors set the given colors.

    Args:
          name (str): The name of the color palette.
        color1 (str): A hex color code.
        color2 (str): A hex color code.
        color3 (str): A hex color code.
        color4 (str): A hex color code.

    Returns:
        None
    """
    global COLOR_PALETTES
    # Check if the color palette is already in the COLOR_PALETTES dictionary
    if name in COLOR_PALETTES:
        colors = COLOR_PALETTES[name]
    # If not, then create a new entry in the COLOR_PALETTES dictionary
    else:
        colors = {}
    # Update the different colors if they have been given as input
    if not color1 is None:
        color1 = color1.split("#")[-1]
        colors["color_page_head_hex"] = "#" + color1
        colors["color_page_head_rgb"] = rgb(color1)
    if not color2 is None:
        color2 = color2.split("#")[-1]
        colors["color_page_body_hex"] = "#" + color2
        colors["color_page_body_rgb"] = rgb(color2)
    if not color3 is None:
        color3 = color3.split("#")[-1]
        colors["color_page_text_1_hex"] = "#" + color3
        colors["color_page_text_1_rgb"] = rgb(color3)
    if not color4 is None:
        color4 = color4.split("#")[-1]
        colors["color_page_text_2_hex"] = "#" + color4
        colors["color_page_text_2_rgb"] = rgb(color4)
    COLOR_PALETTES.update({name: colors})


#------------------------------------------------------------------------------#
#                            Pre-defined color palettes                        #
#------------------------------------------------------------------------------#
# Pre-defined styling / color palette 1: "color_palette_1"
color1 = "717171"; color2 = "ffffff"; color3 = "8939a8"; color4 = "000000"
update_color_palettes("color_palette_1", color1, color2, color3, color4)

#------------------------------------------------------------------------------#
# Pre-defined styling / color palette 2: "color_palette_2"
color1 = "ffffff"; color2 = "616161"; color3 = "36e634"; color4 = "ffffff"
update_color_palettes("color_palette_2", color1, color2, color3, color4)

#------------------------------------------------------------------------------#
# Pre-defined styling / color palette 3: "color_palette_4"
color1 = "3b6978"; color2 = "204051"; color3 = "84a9ac"; color4 = "ffffff"
update_color_palettes("color_palette_3", color1, color2, color3, color4)

#------------------------------------------------------------------------------#
# Pre-defined styling / color palette 4: "color_palette_4"
color1 = "ffffff"; color2 = "393e46"; color3 = "76ead7"; color4 = "ffffff"
update_color_palettes("color_palette_4", color1, color2, color3, color4)
