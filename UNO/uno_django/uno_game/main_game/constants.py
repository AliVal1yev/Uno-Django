class COLOR:
    # BLUE_PREFIX = "\033[97;44m"
    # YELLOW_PREFIX = "\033[43m"
    # RED_PREFIX = "\033[41m"
    # GREEN_PREFIX = "\033[42m"
    # BLACK_PREFIX = "\033[97;40m"
    # COLOR_SUFFIX = "\033[0m"

    # COLOR_DATA = {
    #     "blue": BLUE_PREFIX,
    #     "yellow": YELLOW_PREFIX,
    #     "red": RED_PREFIX,
    #     "green": GREEN_PREFIX,
    #     "black": BLACK_PREFIX
    # }

    MAIN_COLORS = ["blue", "yellow", "red", "green"]

class CARD:
    NUMERIC = "NUMERIC"
    ACTION = "ACTION"
    WILD = "WILD"

    CARD_TYPES = (
        NUMERIC,
        ACTION,
        WILD,
    )

    ACTION_REVERSE_BODY = "⇅"
    ACTION_DRAW_2_BODY = "+2"
    ACTION_SKIP_BODY = "⊘"
    
    ACTION_CARD_TYPES = (
        ACTION_REVERSE_BODY,
        ACTION_DRAW_2_BODY,
        ACTION_SKIP_BODY
    )

    WILD_DRAW_4_BODY = "+4"
    WILD_UNIVERSAL = "⊕"

    WILD_CARD_TYPES = (
        WILD_DRAW_4_BODY,
        WILD_UNIVERSAL
    )