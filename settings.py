# Display settings
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 120
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Images
BG_IMAGE_PATH = 'graphics/0/bg.png'
GRID_IMAGE_PATH = 'graphics/0/gridline.png'
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of play area
SYM_PATH = 'graphics/0/symbols'

# Text
TEXT_COLOR = 'White'
# You need to provide your own font in the below directory
# I downloaded Kidspace font from https://www.dafont.com/kidspace.font
UI_FONT = 'graphics/font/super_shiny.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# 5 Symbols for demo
# symbols = {
#     'diamond': f"{SYM_PATH}/0_diamond.png",
#     'floppy': f"{SYM_PATH}/0_floppy.png",
#     'hourglass': f"{SYM_PATH}/0_hourglass.png",
#     'seven': f"{SYM_PATH}/0_seven.png",
#     'telephone': f"{SYM_PATH}/0_telephone.png"
# }

# 4 Symbols for more wins
symbols = {
    '0_diamond': f"{SYM_PATH}/0_diamond.png",
    '0_floppy': f"{SYM_PATH}/0_floppy.png",
    '0_hourglass': f"{SYM_PATH}/0_hourglass.png",
    '0_kristof': f"{SYM_PATH}/0_kristof.png",
    '0_telephone': f"{SYM_PATH}/0_telephone.png"
}

symbol_payout_multipliers = {
    '0_diamond': 3,
    '0_floppy': 1,
    '0_hourglass': 1,
    '0_kristof': 5,
    '0_telephone': 1
}

symbol_weights = {
    '0_diamond': 2,  # Default weight (least likely)
    '0_floppy': 3,    # Slightly more likely
    '0_hourglass': 3,   # Same weight as floppy
    '0_kristof': 3,   # Kristof symbol is more likely (higher weight)
    '0_telephone': 3  # Moderate weight
}
