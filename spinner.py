#!/usr/bin/env python3
"""
Class for a text spinner.
"""
from typing import Optional, Final
from colours import Colours

STYLES: Final[dict[str, list[str]]] = {
    'segmented_circle': ['\u25F4', '\u25F7', '\u25F6', '\u25F5'],  # Segmented circle
    'arc': ['\u25DC', '\u25DD', '\u25DE', '\u25DF'],  # Arc
    'ascii': ['|', '/', '-', '\\'],  # Ascii
    'half_circle': ['\u25D0', '\u25D3', '\u25D1', '\u25D2'],  # Half circle
    'square_1': ['\u2599', '\u259B', '\u259C', '\u259F'],  # Square 1
    'square_2': ['\u2598', '\u259D', '\u2597', '\u2596'],  # Square 2
    'square_3': ['\u2598', '\u2580', '\u259C', '\u2588', '\u259F', '\u2584', '\u2596', ' '],  # Square 3
    'fade': [' ', '\u2591', '\u2592', '\u2593', '\u2588', '\u2593', '\u2592', '\u2591'],  # Fade in / out
    'vertical_bar': [' ', '\u2581', '\u2582', '\u2583', '\u2584', '\u2585', '\u2586', '\u2587', '\u2588',
                     '\u2587', '\u2586', '\u2585', '\u2584', '\u2583', '\u2582', '\u2581'],  # Vertical
    'horizontal_bar': [' ', '\u258F', '\u258E', '\u258D', '\u258C', '\u258B', '\u258A', '\u2589', '\u2588',
                       '\u2589', '\u258A', '\u258B', '\u258C', '\u258D', '\u258E', '\u258F'],  # Horizontal
    'segmented_square': ['\u25F0', '\u25F3', '\u25F2', '\u25F1'],  # Segmented square.
    'triangle_1': ['\u25E4', '\u25E5', '\u25E2', '\u25E3'],  # Triangle 1.
    'triangle_2': ['\u25F8', '\u25F9', '\u25FF', '\u25FA'],  # Triangle 2.
    'triangle_3': ['\u25B2', '\u25B6', '\u25BC', '\u25C0'],  # Triangle 3.
    'triangle_4': ['\u25B3', '\u25B7', '\u25BD', '\u25C1'],  # Triangle 4.
    'triangle_5': ['\u25B4', '\u25B8', '\u25BE', '\u25C2'],  # Triangle 5.
    'triangle_6': ['\u25B5', '\u25B9', '\u25BF', '\u25C3'],  # Triangle 6.
    'count_up_1': ['\u278A', '\u278B', '\u278C', '\u278D', '\u278E', '\u278F', '\u2790', '\u2791', '\u2792',
                   '\u2793'],  # Count up 1.
    'count_up_2': ['\u2780', '\u2781', '\u2782', '\u2783', '\u2784', '\u2785', '\u2786', '\u2787', '\u2788',
                   '\u2789'],  # Count up 2.
    'count_up_3': ['\u2776', '\u2777', '\u2778', '\u2779', '\u277A', '\u277B', '\u277C', '\u277D', '\u277E',
                   '\u277F'],  # Count up 3.
    'count_up_4': ['\u24F5', '\u24F6', '\u24F7', '\u24F8', '\u24F9', '\u24FA', '\u24FB', '\u24FC', '\u24FD',
                   '\u24FE'],  # Count up 4.
    'count_up_5': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],  # Count up 5.
    'count_up_6': ['\u2474', '\u2475', '\u2476', '\u2477', '\u2478', '\u2479', '\u247A', '\u247B', '\u247C',
                   '\u247D', '\u247E', '\u247F', '\u2480', '\u2481', '\u2482', '\u2483', '\u2484', '\u2485',
                   '\u2486', '\u2487'],  # Count up 6.
    'count_down_1': ['\u2793', '\u2792', '\u2791', '\u2790', '\u278F', '\u278E', '\u278D', '\u278C', '\u278B',
                     '\u278A'],  # Count down 1.
    'count_down_2': ['\u2789', '\u2788', '\u2787', '\u2786', '\u2785', '\u2784', '\u2783', '\u2782', '\u2781',
                     '\u2780'],  # Count down 2.
    'count_down_3': ['\u277F', '\u277E', '\u277D', '\u277C', '\u277B', '\u277A', '\u2779', '\u2778', '\u2777',
                     '\u2776'],  # Count down 3.
    'count_down_4': ['\u24FE', '\u24FD', '\u24FC', '\u24FB', '\u24FA', '\u24F9', '\u24F8', '\u24F7', '\u24F6',
                     '\u24F5'],  # Count down 4.
    'count_down_5': ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0'],  # Count down 5.
    'count_down_6': ['\u2487', '\u2486', '\u2485', '\u2484', '\u2483', '\u2482', '\u2481', '\u2480', '\u247F',
                     '\u247E', '\u247D', '\u247C', '\u247B', '\u247A', '\u2479', '\u2478', '\u2477', '\u2476',
                     '\u2475', '\u2474'],  # Count down 6.
    'line': ['\u2502', '\u2571', '\u2500', '\u2572'],  # Line.
    'upper_four_dots': ['\u2802', '\u2801', '\u2808', '\u2810'],  # Upper four dots.
    'upper_four_dots_reverse': ['\u2819', '\u281A', '\u2813', '\u280B'],  # Upper four dots, reversed.
    'upper_four_dots_bar': ['\u2800', '\u2812', '\u281B', '\u2812'],  # Upper four dots bar.
    'middle_four_dots': ['\u2804', '\u2802', '\u2810', '\u2820'],  # Middle four dots.
    'middle_four_dots_reverse': ['\u2832', '\u2834', '\u2826', '\u2816'],  # Middle four dots, reversed.
    'middle_four_dots_bar': ['\u2800', '\u2824', '\u2836', '\u2824'],  # Middle four dots, bar.
    'lower_four_dots': ['\u2840', '\u2804', '\u2820', '\u2880'],  # Lower four dots.
    'lower_four_dots_reverse': ['\u28A4', '\u28E0', '\u28C4', '\u2864'],  # Lower four dots, reversed.
    'lower_four_dots_bar': ['\u2800', '\u28C0', '\u28E4', '\u28C0'],  # Lower four dots, bar.
    'six_dots': ['\u2804', '\u2802', '\u2801', '\u2808', '\u2810', '\u2820'],  # Six dots.
    'six_dots_reverse': ['\u283b', '\u283D', '\u283E', '\u2837', '\u282F', '\u281F'],  # Six dots reverse.
    'six_dots_bar': ['\u2800', '\u2824', '\u2836', '\u283F', '\u2836', '\u2824'],  # Six dots bar.
    'six_dots_build': ['\u2800', '\u2804', '\u2806', '\u2807', '\u280F', '\u281F', '\u283F', '\u283B', '\u2839',
                       '\u2807', '\u2806', '\u2804'],  # Six dots build.
    'eight_dots': ['\u2840', '\u2804', '\u2802', '\u2801', '\u2808', '\u2810', '\u2820', '\u2880'],  # Eight dots.
    'eight_dots_reverse': ['\u28BF', '\u28FB', '\u28FD', '\u28FE', '\u28F7', '\u28EF', '\u28DF', '\u287F'],
    # Eight dots reverse.
    'eight_dots_bar': ['\u2800', '\u28C0', '\u28E4', '\u28F6', '\u28FF', '\u28F6', '\u28E4', '\u28C0'],
    # Eight dots bar
    'eight_dots_build': ['\u2800', '\u2840', '\u2844', '\u2846', '\u2847', '\u284F', '\u285F', '\u287F', '\u28FF',
                         '\u28BF', '\u28BB', '\u28B9', '\u28B8', '\u28B0', '\u28A0', '\u2880'],  # Eight dots build.

}

NUM_STYLES: Final[int] = len(STYLES.keys())
# Style Consts
STYLE_SEGMENTED_CIRCLE: Final[str] = 'segmented_circle'
STYLE_ARC: Final[str] = 'arc'
STYLE_ASCII: Final[str] = 'ascii'
STYLE_HALF_CIRCLE: Final[str] = 'half_circle'
STYLE_SQUARE_1: Final[str] = 'square_1'
STYLE_SQUARE_2: Final[str] = 'square_2'
STYLE_SQUARE_3: Final[str] = 'square_3'
STYLE_FADE: Final[str] = 'fade'
STYLE_VERTICAL_BAR: Final[str] = 'vertical_bar'
STYLE_HORIZONTAL_BAR: Final[str] = 'horizontal_bar'
STYLE_SEGMENTED_SQUARE: Final[str] = 'segmented_square'
STYLE_TRIANGLE_1: Final[str] = 'triangle_1'
STYLE_TRIANGLE_2: Final[str] = 'triangle_2'
STYLE_TRIANGLE_3: Final[str] = 'triangle_3'
STYLE_TRIANGLE_4: Final[str] = 'triangle_4'
STYLE_TRIANGLE_5: Final[str] = 'triangle_5'
STYLE_TRIANGLE_6: Final[str] = 'triangle_6'
STYLE_COUNT_UP_1: Final[str] = 'count_up_1'
STYLE_COUNT_UP_2: Final[str] = 'count_up_2'
STYLE_COUNT_UP_3: Final[str] = 'count_up_3'
STYLE_COUNT_UP_4: Final[str] = 'count_up_4'
STYLE_COUNT_UP_5: Final[str] = 'count_up_5'
STYLE_COUNT_UP_6: Final[str] = 'count_up_6'
STYLE_COUNT_DOWN_1: Final[str] = 'count_down_1'
STYLE_COUNT_DOWN_2: Final[str] = 'count_down_2'
STYLE_COUNT_DOWN_3: Final[str] = 'count_down_3'
STYLE_COUNT_DOWN_4: Final[str] = 'count_down_4'
STYLE_COUNT_DOWN_5: Final[str] = 'count_down_5'
STYLE_COUNT_DOWN_6: Final[str] = 'count_down_6'
STYLE_LINE: Final[str] = 'line'
STYLE_UPPER_FOUR_DOTS_REVERSE: Final[str] = 'upper_four_dots'
STYLE_MIDDLE_FOUR_DOTS_REVERSE: Final[str] = 'middle_four_dots'
STYLE_LOWER_FOUR_DOTS_REVERSE: Final[str] = 'lower_four_dots'
STYLE_SIX_DOTS: Final[str] = 'six_dots'
STYLE_SIX_DOTS_REVERSE: Final[str] = 'six_dots_reverse'
STYLE_SIX_DOTS_BAR: Final[str] = 'six_dots_bar'
STYLE_EIGHT_DOTS: Final[str] = "eight_dots"
STYLE_EIGHT_DOTS_REVERSE: Final[str] = 'eight_dots_reverse'
STYLE_EIGHT_DOTS_BAR: Final[str] = 'eight_dots_bar'
STYLE_EIGHT_DOTS_BUILD: Final[str] = 'eight_dots_build'


class SpinnerError(Exception):
    """Class to store spinner errors."""
    _errorMessages: Final[dict[int, str]] = {
        0: 'No error.',
        1: 'TypeError: style_name must be a str.',
        2: 'ValueError: style_name is not a valid style name.',
        3: 'TypeError: fg_colour must be a str or None.',
        4: 'ValueError: fg_colour must be a valid foreground colour string.',
        5: 'TypeError: bg_colour must be a str or None.',
        6: 'ValueError: bg_colour must be a valid background colour string.',
        7: 'TypeError: bold must be a bool.',
        8: 'TypeError: underline must be a bool.',
        9: 'TypeError: reverse must be a bool.',
        10: 'TypeError: strike_through must be a bool.',
        11: 'TypeError: length must be an int.',
        12: 'ValueError: length must be greater than zero.',
        13: 'TypeError: fill_character must be a str.',
        14: 'ValueError: fill_character must be a single character.',
        15: 'TypeError: alignment_character must be a str.',
        16: 'ValueError: alignment_character must be: "<", "^", ">".',
        17: 'TypeError: clockwise must be a bool.',
        18: 'TypeError: completed_character must be a str.',
        19: 'ValueError: completed_character must be a less than or equal to length property.',
        20: 'TypeError: step must be an int.',
        21: 'ValueError: step out of range.',
        22: 'TypeError: increment_step must be a bool.',
        23: 'TypeError: do_print must be a bool.',
        24: 'TypeError: end must be a str.',
        25: 'TypeError: completed must be a bool.',

    }

    def __init__(self, error_number: int, *args: object) -> None:
        super().__init__(*args)
        self.error_number = error_number
        self.error_message = self._errorMessages[error_number]
        return


class Spinner(object):
    """
    Class to print a text spinner.
        Properties:
            style_name: str
            step: int
            max_step: int (read only)
            fg_colour: Optional[str]
            bg_colour: Optional[str]
            bold: bool
            underline: bool
            reverse: bool
            strike_through: bool
            length: int
            fill_character: str
            alignment_character: str one of [ '<', '^', '>' ].
            clockwise: bool
            completed_character: str
            complete: bool
        Methods:
            increment_step()
            print()
    """

    ########
    # Initialize:
    ########
    def __init__(self,
                 style_name: str = STYLE_ASCII,
                 fg_colour: Optional[str] = None,
                 bg_colour: Optional[str] = None,
                 bold: bool = False,
                 underline: bool = False,
                 reverse: bool = False,
                 strike_through: bool = False,
                 length: int = 1,
                 alignment_character: str = '^',
                 fill_character: str = ' ',
                 clock_wise: bool = True,
                 completed_character: str = '\u2714',
                 ) -> None:
        """
        Initialize the spinner.
        :param style_name: str: The style name of the spinner, defaults to STYLE_ASCII
        :param fg_colour: Optional[str]: The foreground colour. Defaults to None.
        :param bg_colour: Optional[str]: The background colour. Defaults to None
        :param bold: bool: Use bold font. Defaults to False.
        :param underline: bool: Use underlining. Defaults to False.
        :param reverse: bool: Use reverse colours. Defaults to False.
        :param strike_through: bool: Use strike through font. Defaults to False.
        :param length: int: Return / print a string of this many characters. Defaults to 1.
        :param alignment_character: str: The fstring alignment character. Defaults to '^' (center). Valid characters
                                            are: '<', '^', and '>'. Only effects multi-character strings.
        :param fill_character: str: The character to use to fill when length > 1. Defaults to ' ' (space).
        :param clock_wise: bool: The direction to spin / count. True = clockwise / count up. False = counter-clockwise /
                                    count down.
        :param completed_character:
        """
        # Argument checks:
        # Style:
        if not isinstance(style_name, str):
            raise SpinnerError(1)
        elif style_name not in STYLES.keys():
            raise SpinnerError(2)
        # Foreground Colour:
        if fg_colour is not None and not isinstance(fg_colour, str):
            raise SpinnerError(3)
        elif fg_colour is not None and not Colours.is_foreground(fg_colour):
            raise SpinnerError(4)
        # Background Colour:
        if bg_colour is not None and not isinstance(bg_colour, str):
            raise SpinnerError(5)
        elif bg_colour is not None and not Colours.is_background(bg_colour):
            raise SpinnerError(6)
        # Bold:
        if not isinstance(bold, bool):
            raise SpinnerError(7)
        # Underline:
        if not isinstance(underline, bool):
            raise SpinnerError(8)
        # Reverse:
        if not isinstance(reverse, bool):
            raise SpinnerError(9)
        # Strike through:
        if not isinstance(strike_through, bool):
            raise SpinnerError(10)
        # Length:
        if not isinstance(length, int):
            raise SpinnerError(11)
        elif length < 1:
            raise SpinnerError(12)
        # Fill character:
        if not isinstance(fill_character, str):
            raise SpinnerError(13)
        elif len(fill_character) != 1:
            raise SpinnerError(14)
        # Alignment character:
        if not isinstance(alignment_character, str):
            raise SpinnerError(15)
        elif alignment_character not in ('<', '^', '>'):
            raise SpinnerError(16)
        # Clock wise:
        if not isinstance(clock_wise, bool):
            raise SpinnerError(17)
        # Completed Character:
        if not isinstance(completed_character, str):
            raise SpinnerError(18)
        elif len(completed_character) != 1:
            raise SpinnerError(19)
        # Set properties:
        self._style_name: str = style_name
        self._step: int = 0
        self._max_step: int = len(STYLES[style_name]) - 1
        self._fg_colour: Optional[str] = fg_colour
        self._bg_colour: Optional[str] = bg_colour
        self._bold: bool = bold
        self._underline: bool = underline
        self._reverse: bool = reverse
        self._strike_through: bool = strike_through
        self._length: int = length
        self._fill_character: str = fill_character
        self._alignment_character: str = alignment_character
        self._clockwise: bool = clock_wise
        self._completed_character: str = completed_character
        self._complete: bool = False
        return

    ########
    # Properties:
    ########
    @property
    def style_name(self) -> str:
        """
        Get the style name.
        :return: str: The style name.
        """
        return self._style_name

    @style_name.setter
    def style_name(self, value: str) -> None:
        """
        Set the style name.
        :param value: str: The name of the style.
        :return: None
        :raises: SpinnerError on value type error or value not valid style name.
        """
        if not isinstance(value, str):
            raise SpinnerError(1)
        elif value not in STYLES.keys():
            raise SpinnerError(2)
        self._style_name = value
        self._max_step = len(STYLES[value]) - 1
        if self._step > self._max_step:
            self._step = self._max_step
        return

    @property
    def step(self) -> int:
        """
        Get the current step.
        :return: int: The current step.
        """
        return self._step

    @step.setter
    def step(self, value: int) -> None:
        """
        Set the current step.
        :param value: int: The current step.
        :return: None
        :raises: SpinnerError on value type error or value out of valid range for current style.
        """
        if not isinstance(value, int):
            raise SpinnerError(20)
        if value < 0 or value > self._max_step:
            raise SpinnerError(21)
        self._step = value
        return

    @property
    def max_step(self) -> int:
        """
        Get the max step value for the current style.
        :return: int: The max step.
        """
        return self._max_step

    @property
    def fg_colour(self) -> Optional[str]:
        """
        Gets the foreground colour.
        :return: Optional[str]: The foreground colour string, or None.
        """
        return self._fg_colour

    @fg_colour.setter
    def fg_colour(self, value: Optional[str]) -> None:
        """
        Sets the foreground colour.
        :param value: Optional[str]: The foreground colour string or None.
        :return: None
        :raises: SpinnerError on value type error or value is not valid foreground colour string.
        """
        if value is not None and not isinstance(value, str):
            raise SpinnerError(3)
        elif not Colours.is_foreground(value):
            raise SpinnerError(4)
        self._fg_colour = value
        return

    @property
    def bg_colour(self) -> Optional[str]:
        """
        Gets the background colour.
        :return: Optional[str]: The background colour string, or None.
        """
        return self._bg_colour

    @bg_colour.setter
    def bg_colour(self, value: Optional[str]) -> None:
        """
        Set the background colour.
        :param value: Optional[str]: The background colour string or None.
        :return: None
        :raises: SpinnerError on value type error or value is not valid background colour string.
        """
        if value is not None and not isinstance(value, str):
            raise SpinnerError(5)
        elif not Colours.is_background(value):
            raise SpinnerError(6)
        self._bg_colour = value
        return

    @property
    def bold(self) -> bool:
        """
        Get if bold font is being used.
        :return: bool: True = bold; False = No bold.
        """
        return self._bold

    @bold.setter
    def bold(self, value: bool) -> None:
        """
        Sets the use of bold font.
        :param value: bool: True = use bold; False = do not use bold.
        :return: None
        :raises: SpinnerError on value type error.
        """
        if not isinstance(value, bool):
            raise SpinnerError(7)
        self._bold = value
        return

    @property
    def underline(self) -> bool:
        """
        Get if underlining is being used.
        :return: bool: True = underline; False = No underline.
        """
        return self._underline

    @underline.setter
    def underline(self, value: bool) -> None:
        """
        Sets the use of underlining.
        :param value: bool: True = Use underlining; False = Do not use underlining.
        :return: None
        :raises: SpinnerError on value type error.
        """
        if not isinstance(value, bool):
            raise SpinnerError(8)
        self._underline = value
        return

    @property
    def reverse(self) -> bool:
        """
        Get if reverse colours are being used.
        :return: bool: True = Colours reversed; False = Colours are normal.
        """
        return self._reverse

    @reverse.setter
    def reverse(self, value: bool) -> None:
        """
        Sets the use of reverse colours.
        :param value: bool: True = Use reverse colours; False = Use normal colours.
        :return: None
        :raises: SpinnerError on value type error.
        """
        if not isinstance(value, bool):
            raise SpinnerError(9)
        self._reverse = value
        return

    @property
    def strike_through(self) -> bool:
        """
        Gets if using strike through font.
        :return: bool: True = Use strike through; False = Do not use strike through.
        """
        return self._strike_through

    @strike_through.setter
    def strike_through(self, value: bool) -> None:
        """
        Sets the use of strike through.
        :param value: bool: True = Use strike through; False = Do not use strike through.
        :return: None
        :raises: Spinner error on value type error.
        """
        if not isinstance(value, bool):
            raise SpinnerError(10)
        self._strike_through = value
        return

    @property
    def length(self) -> int:
        """
        Gets the length of the string printed / returned.
        :return: int: The length of the string printed / returned.
        """
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        """
        Sets the length of the string printed / returned.
        :param value: int: The length of the string printed / returned.
        :return: None
        :raises: SpinnerError on value type error or if value <= 0.
        """
        if not isinstance(value, int):
            raise SpinnerError(11)
        elif value < 1:
            raise SpinnerError(12)
        self._length = value
        return

    @property
    def fill_character(self) -> str:
        """
        Get the fill character.
        :return: str: The fill character.
        """
        return self._fill_character

    @fill_character.setter
    def fill_character(self, value: str) -> None:
        """
        Sets the fill character used when length > 1.
        :param value: str: The fill character.
        :return: None
        :raises: SpinnerError on value type error or value len != 1.
        """
        if not isinstance(value, str):
            raise SpinnerError(13)
        elif len(value) != 1:
            raise SpinnerError(14)
        self._fill_character = value
        return

    @property
    def alignment_character(self) -> str:
        """
        Gets the alignment character to use with fstring.
        :return: str: The alignment character.
        """
        return self._alignment_character

    @alignment_character.setter
    def alignment_character(self, value: str) -> None:
        """
        Sets the alignment character.
        :param value: str: The alignment character, valid values are '<', '^', and '>'.
        :return: None
        :raises: SpinnerError on value type error, or if not valid value.
        """
        if not isinstance(value, str):
            raise SpinnerError(15)
        elif len(value) != 1:
            raise SpinnerError(16)
        elif value not in ('<', '^', '>'):
            raise SpinnerError(16)
        self._alignment_character = value
        return

    @property
    def clockwise(self) -> bool:
        """
        Gets spinner / count direction.
        :return: bool: True = clockwise / count up; False = counter-clockwise / count down.
        """
        return self._clockwise

    @clockwise.setter
    def clockwise(self, value:bool) -> None:
        """
        Sets the spinner / count direction.
        :param value: bool: True = Clockwise / count up; False = Counter-clockwise / count down.
        :return: None
        :raises: SpinnerError on value type error.
        """
        if not isinstance(value, bool):
            raise SpinnerError(17)
        self._clockwise = value
        return

    @property
    def completed_character(self) -> str:
        """
        Get the character(s) to show when completed property is set to True.
        :return: str: The completed character.
        """
        return self._completed_character

    @completed_character.setter
    def completed_character(self, value: str) -> None:
        """
        Sets the character(s) to show when completed property is set to True.
        :param value: str: The character(s) to show.
        :return: None
        :raises: SpinnerError on value type error, or if len(value) > length.
        """
        if not isinstance(value, str):
            raise SpinnerError(18)
        elif len(value) > self._length:
            raise SpinnerError(19)
        self._completed_character = value
        return

    @property
    def complete(self) -> bool:
        """
        The completed flag, when set shows completed character(s).
        :return: bool: The completed flag. True = show completed characters; False = Show current step characters.
        """
        return self._complete

    @complete.setter
    def complete(self, value: bool) -> None:
        """
        Set the completed flag.
        :param value: bool: True = Shows completed character(s); False = Show spinner step character.
        :return: None
        :raises: SpinnerError on value type error.
        """
        if not isinstance(value, bool):
            raise SpinnerError(25)
        self._complete = value
        return

    ########
    # Helpers:
    ########
    def increment_step(self) -> int:
        """
        Increment the step.
        :return: int: The step before incrementing.
        """
        old_value: int = self._step
        self._step += 1
        if self._step > self._max_step:
            self._step = 0
        return old_value

    ########
    # Output:
    ########

    def print(self,
              increment_step: bool = True,
              do_print: bool = True,
              use_colour: bool = True,
              end: str = '',
              **kw_args,
              ) -> str:
        """
        Print the current step, and increment step if requested.
        :param increment_step: bool: Increment the step, wrapping if required. Defaults to True.
        :param do_print: bool: Print the string, if True. If False, ignores end, colours, and kw_args. Defaults to True.
        :param use_colour: bool: Print the colour strings if True. If False, colours will be ignored. Defaults to True.
        :param end: str: What to pass to print for the end parameter. Defaults to '' (empty string).
        :param kw_args: dict: Additional key word args to pass to print.
        :return: str: The spinner string.
        """
        # Argument checks:
        # Increment step:
        if not isinstance(increment_step, bool):
            raise SpinnerError(22)
        # do print:
        if not isinstance(do_print, bool):
            raise SpinnerError(23)
        # End:
        if not isinstance(end, str):
            raise SpinnerError(24)
        # Determine spinner string:
        # Determine direction:
        step_index = self._step
        if not self._clockwise:
            step_index = -step_index - 1
        # Set character
        if self._complete:
            spinner_char = self._completed_character
        else:
            spinner_char: str = STYLES[self._style_name][step_index]
        # Generate format string:
        f_string = "{character:%s%s%is}" % (self._fill_character, self._alignment_character, self._length)
        # Generate spinner string:
        spinner_string = f_string.format(character=spinner_char)
        # Print colour strings if requested:
        if do_print and use_colour:
            # Print foreground colour:
            if self._fg_colour is not None:
                print(self._fg_colour, end='', **kw_args)
            # Print background colour:
            if self._bg_colour is not None:
                print(self._bg_colour, end='', **kw_args)
            # Print bold:
            if self._bold:
                print(Colours.bold, end='', **kw_args)
            # Print underline:
            if self._underline:
                print(Colours.underline, end='', **kw_args)
            # Print reverse:
            if self._reverse:
                print(Colours.reverse, end='', **kw_args)
            # Print strike through:
            if self._strike_through:
                print(Colours.strikeThrough, end='', **kw_args)
            # Print spinner character:
            print(spinner_string, end='', **kw_args)
            # Reset the Colours:
            if do_print and use_colour:
                print(Colours.reset, end=end, **kw_args)
        # Increment step:
        if increment_step:
            self.increment_step()
        # Return:
        return spinner_string


######################################################################
def run_test(spinner: Spinner, spinner2: Optional[Spinner] = None):
    if spinner.style_name.startswith('count'):
        for i in range(20):
            print("\r", end='')
            print(" step:%2i  " % spinner.step, end='')
            spinner.print()
            if spinner2 is not None:
                spinner2.print()
            sleep(0.5)
        spinner.complete = True
        print("\r", end='')
        print(" step:%2i " % spinner.step, end='')
        spinner.print()
        spinner.complete = False
    else:
        for i in range(50):
            print("\r", end='')
            print(" step:%2i " % spinner.step, end='')
            spinner.print()
            if spinner2 is not None:
                spinner2.print()
            sleep(0.1)
        spinner.complete = True
        print("\r", end='')
        print(" step:%2i " % spinner.step, end='')
        spinner.print()
    return


if __name__ == '__main__':
    from time import sleep

    # Select style:
    while (True):
        index: str = "Index:"
        key: str = "Name:"
        title: str = f"{index:~^10s}\t{key:~^25s}"
        print(title + "\t" + title)
        lines = []
        firstColMax = NUM_STYLES // 2
        if NUM_STYLES % 2:
            firstColMax += 0
        else:
            firstColMax -= 1
        for i in range(firstColMax + 1):
            idx = "%02i" % i
            name = list(STYLES.keys())[i]
            line = f"{idx:^10s}\t{name:<25s}"
            line += "\t"
            lines.append(line)
        for i in range(firstColMax + 1, NUM_STYLES):
            idx = "%02i" % i
            index = i - firstColMax - 1
            name = list(STYLES.keys())[i]
            lines[index] += f"{idx:^10s}\t{name:<25s}"
        #     lines.append(line)
        for line in lines:
            print(line)
        # exit(0)
        response = input("Select style: ")
        if response in STYLES.keys():
            break
        try:
            response = int(response)
        except ValueError as e:
            print("Please enter a number, or style name.")
            sleep(1)
            continue
        if response < 0 or response >= NUM_STYLES:
            print("Invalid selection.")
            sleep(1)
            continue
        break

    # Determine style name:
    styleName: str
    if isinstance(response, int):
        styleName = list(STYLES.keys())[response]
    else:
        styleName = response
    spinner: Spinner = None
    spinner2: Optional[Spinner] = None
    # Create the spinner:
    spinner = Spinner(
        style_name=styleName,
        fg_colour=Colours.fg.light_green,
        bg_colour=Colours.bg.black,
        bold=True,
        underline=True,
        length=5,
        fill_character=' ',
        alignment_character='<',
        clock_wise=True,
    )
    print(f"Spinner test: clockwise: '{styleName:s}'")

    run_test(spinner)
    spinner.complete = False
    spinner.clockwise = False
    spinner.alignment_character = '^'
    print()
    print(f"Spinner test: counter clockwise: '{styleName:s}'")
    run_test(spinner)

    print()
