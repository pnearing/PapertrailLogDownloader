#!/usr/bin/env python3
"""File colours.py"""
from typing import Match, Final, Pattern
import re

# Initial control character:
_control_character: Final[str] = '\033'
# Regex to validate basic colour / control strings.
_is_four_bit_regex: Pattern = re.compile(r'^\033\[(?P<value>\d+)m$')
_is_eight_bit_regex: Pattern = re.compile(r'^\033\[(?P<fgBg>[34]8);5;(?P<value>\d{1,3})m$')
_is_sixteen_bit_regex: Pattern = re.compile(r'^\033\[(?P<fgBg>[34]8);2;(?P<red>\d{1,3});(?P<green>\d{1,3});(?P<blue>\d{1,3})m$')
# List of valid 4 bit control values.
_control_values: Final[list[str]] = [
    '0', '01', '02', '03', '04', '05', '06', '07', '08', '09'
]
# List of valid 4 bit foreground colour values.
_four_bit_fg_values: Final[list[str]] = [
    '30', '31', '32', '33', '34', '35', '36', '37', '90', '91', '92', '93', '94', '95', '96', '97'
]
# List of valid 4 bit background colour values.
_four_bit_bg_values: Final[list[str]] = [
    '40', '41', '42', '43', '44', '45', '46', '47', '100', '101', '102', '103', '104', '105', '106', '107'
]
# Valid 8 bit foreground / background values:
_eight_bit_fg_value: Final[str] = '38'
_eight_bit_bg_value: Final[str] = '48'
# Valid 16 bit foreground / background values:
_sixteen_bit_fg_value: Final[str] = '38'
_sixten_bit_bg_value: Final[str] = '48'


def __value_is_valid__(value: str) -> bool:
    str_value = value
    int_value = int(value)
    if 0 <= int_value <= 9:
        if len(str_value) == 1:
            return True
    elif 10 <= int_value <= 99:
        if len(str_value) == 2:
            return True
    elif 100 <= int_value <= 255:
        if len(str_value) == 3:
            return True
    return False


class ColourError(Exception):
    """Class for all colour errors."""
    _errorMessages = {
        0: 'No Error.',
        1: 'TypeError: value must be an int between 0 and 255, inclusive.',
        2: 'TypeError: red must be an int between 0 and 255, inclusive.',
        3: 'TypeError: green must be an int between 0 and 255, inclusive.',
        4: 'TypeError: blue must be an int between 0 and 255, inclusive.',
        5: 'TypeError: value must be a str.',
        6: 'ValueError: value must be an int between 0 and 255, inclusive.',
        7: 'ValueError: red value must be an int between 0 and 255, inclusive.',
        8: 'ValueError: green value must be an int between 0 and 255, inclusive.',
        9: 'ValueError: blue value must be an int between 0 and 255, inclusive.',
        10: 'Value is not valid control string.',
        11: 'Value is not valid colour string.',
        12: 'Value is not valid four bit colour string.',
        13: 'Value is not valid eight bit colour string.',
        14: 'Value is not valid sixteen bit colour string.',
        15: 'Value is not valid foreground colour string.',
        16: 'Value is not valid background colour string.',
    }

    def __init__(self,
                 error_number: int,
                 *args: object
                 ) -> None:
        """
        Initialize the error.
        :param error_number: int, The error message number.
        :param args: object, Additional arguments to pass to Exception.
        """
        super().__init__(*args)
        self.error_number: int = error_number
        self.error_message: str = self._errorMessages[error_number]
        return


class Colours(object):
    """
    Classes and methods to store and generate, and validate colour / control strings.
        Class: Colours(object), Stores control strings by name, and validation methods.
            Class: Colours.ColourError(Exception)
            Method: Colours.is_control(value, raiseOnError), Return True if value is valid 4-Bit control string.
            Method: Colours.is_colour(value, raiseOnError), Return True if value is valid colour string, regardless of
                                                                bit length.
            Method: Colours.is_four_bit(value, raiseOnError), Return True if value is valid 4-Bit colour string.
            Method: Colours.is_eight_bit(value, raiseOnError), Return True if value is valid 8-Bit colour string.
            Method: Colours.is_sixteen_bit(value, raiseOnError), Return True if value is valid 16-Bit colour string.
            Method: Colours.is_foreground(value, raiseOnError), Return True if value is valid foreground colour string.
            Method: Colours.is_background(value, raiseOnError), Return True if value is valid background colour string.
            Class: Colours.fg(object), Stores 4-Bit foreground colour values by name.
                Method: Colours.fg.colour(value), Generate an 8-Bit foreground colour string, given colour value.
                Method: Colours.fg.rgb(red, green, blue), Generate a 16-Bit foreground colour string, given red, green,
                                                            and blue values.
            Class: Colours.bg(object), Stores 4-Bit background colour values by name.
                Method: Colours.bg.colour(value), Generate an 8-Bit background colour string, given colour value.
                Method: Colours.bg.rgb(red, green, blue), Generate a 16-Bit background colour string, given red, green,
                                                            and blue values.
    """

    # Control strings:
    reset: Final[str] = '\033[0m'
    bold: Final[str] = '\033[01m'
    disable: Final[str] = '\033[02m'
    underline: Final[str] = '\033[04m'
    blink: Final[str] = '\033[05m'  # Note also '\033[06m'
    reverse: Final[str] = '\033[07m'
    invisible: Final[str] = '\033[08m'
    strikeThrough: Final[str] = '\033[09m'

    @staticmethod
    def is_control(value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is a valid 4-bit control string.
        :param value: str, The value to check.
        :param raise_on_false: Raise ColourError instead of returning False
        :raises ColourError: If raise_on_false is True, and would return False.
        :return: bool: True if value is a valid 4-bit colour value.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(10)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        if four_bit_match is not None:
            if four_bit_match['value'] in _control_values:
                return True
        if raise_on_false:
            raise ColourError(10)
        else:
            return False

    @staticmethod
    def is_four_bit(value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is a valid 4-bit colour string.
        :param value: str, The value to check.
        :param raise_on_false: bool, If true raises ColourError instead of returning False.
        :raises ColourError:If raise_on_false is true, and would return False.
        :return: bool, True if value is valid 4-bit colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(12)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        four_bit_values: list[str] = _four_bit_fg_values + _four_bit_bg_values
        if four_bit_match is not None:
            if four_bit_match['value'] in four_bit_values:
                return True
        if raise_on_false:
            raise ColourError(12)
        else:
            return False

    @staticmethod
    def is_eight_bit(value: object, raise_on_false: bool = False) -> bool:
        """
        Returns True if value is valid 8-Bit colour string.
        :param value: str, The value to check.
        :param raise_on_false: If true raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True, and would return False.
        :return: bool, True if valid 8-bit colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(13)
            else:
                return False
        eight_bit_match: Match = _is_eight_bit_regex.match(value)
        if eight_bit_match is not None:
            if __value_is_valid__(eight_bit_match['value']):
                return True
        if raise_on_false:
            raise ColourError(13)
        else:
            return False

    @staticmethod
    def is_sixteen_bit(value: object, raise_on_false=False) -> bool:
        """
        Return True if value is valid 16-bit colour string.
        :param value: str, The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True, and would return False.
        :return: bool, True if value is a valid 16-bit colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(14)
            else:
                return False
        sixteen_bit_match: Match = _is_sixteen_bit_regex.match(value)
        if sixteen_bit_match is not None:
            red_good = __value_is_valid__(sixteen_bit_match['red'])
            green_good = __value_is_valid__(sixteen_bit_match['green'])
            blue_good = __value_is_valid__(sixteen_bit_match['blue'])
            if red_good is True and green_good is True and blue_good is True:
                return True
        if raise_on_false:
            raise ColourError(14)
        else:
            return False

    @classmethod
    def is_colour(cls, value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is a valid colour string of any bit length.
        :param value: The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: bool, True if valid colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(11)
            else:
                return False
        if cls.is_four_bit(value) is True or cls.is_eight_bit(value) is True or cls.is_sixteen_bit(value) is True:
            return True
        if raise_on_false:
            raise ColourError(11)
        else:
            return False

    @classmethod
    def is_foreground(cls, value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is valid foreground colour of any bit length.
        :param value: The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: bool, True if value is valid foreground colour string.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(15)
            else:
                return False
        if not cls.is_colour(value):
            if raise_on_false:
                raise ColourError(15)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        eight_bit_match: Match = _is_eight_bit_regex.match(value)
        sixteen_bit_match: Match = _is_sixteen_bit_regex.match(value)
        if four_bit_match is not None:
            if four_bit_match['value'] in _four_bit_fg_values:
                return True
        elif eight_bit_match is not None:
            if eight_bit_match['fgBg'] == _eight_bit_fg_value:
                return True
        elif sixteen_bit_match is not None:
            if sixteen_bit_match['fgBg'] == _sixteen_bit_fg_value:
                return True
        if raise_on_false:
            raise ColourError(15)
        else:
            return False

    @classmethod
    def is_background(cls, value: object, raise_on_false: bool = False) -> bool:
        """
        Return True if value is valid background colour of any bit length.
        :param value: The value to check.
        :param raise_on_false: If True, raises ColourError instead of returning False.
        :raises ColourError: If raise_on_false is True and would return False.
        :return: bool, True f valid background colour.
        """
        if not isinstance(value, str):
            if raise_on_false:
                raise ColourError(16)
            else:
                return False
        if not cls.is_colour(value):
            if raise_on_false:
                raise ColourError(16)
            else:
                return False
        four_bit_match: Match = _is_four_bit_regex.match(value)
        eight_bit_match: Match = _is_eight_bit_regex.match(value)
        sixteen_bit_match: Match = _is_sixteen_bit_regex.match(value)
        if four_bit_match is not None:
            if four_bit_match['value'] in _four_bit_bg_values:
                return True
        elif eight_bit_match is not None:
            if eight_bit_match['fgBg'] == _eight_bit_bg_value:
                return True
        elif sixteen_bit_match is not None:
            if sixteen_bit_match['fgBg'] == _sixten_bit_bg_value:
                return True
        if raise_on_false:
            raise ColourError(16)
        else:
            return False

    # Foreground
    class fg(object):
        """Foreground Colours."""
        # 4 bit colour (16 Colours)
        black: Final[str] = '\033[30m'
        red: Final[str] = '\033[31m'
        green: Final[str] = '\033[32m'
        orange: Final[str] = '\033[33m'
        blue: Final[str] = '\033[34m'
        purple: Final[str] = '\033[35m'
        cyan: Final[str] = '\033[36m'
        light_grey: Final[str] = '\033[37m'
        dark_grey: Final[str] = '\033[90m'
        light_red: Final[str] = '\033[91m'
        light_green: Final[str] = '\033[92m'
        yellow: Final[str] = '\033[93m'
        lightblue: Final[str] = '\033[94m'
        pink: Final[str] = '\033[95m'
        light_cyan: Final[str] = '\033[96m'
        white: Final[str] = '\033[97m'

        # 8 bit foreground colour (256 Colours):
        @staticmethod
        def colour(value: int) -> str:
            """
            Get an 8-Bit foreground colour:
            :param value: int, The colour value (0-255).
            :raises ColourError: On type error, or value error.
            :return: str, The 8-bit colour string.
            """
            # Type check:
            if not isinstance(value, int):
                raise ColourError(1)
            # Value check:
            if value < 0 or value > 255:
                raise ColourError(6)
            return '\033[38;5;%im' % value

        # 16 bit foreground colour (65,536 Colours)
        @staticmethod
        def rgb(red: int, green: int, blue: int) -> str:
            """
            Get a 16-Bit foreground colour.
            :param red: int, The red value (0-255).
            :param green: int, The green value (0-255).
            :param blue: int, The blue value (0-255).
            :return: str, The 16-bit colour string.
            """
            # Type check:
            if not isinstance(red, int):
                raise ColourError(2)
            if not isinstance(green, int):
                raise ColourError(3)
            if not isinstance(blue, int):
                raise ColourError(4)
            # Value check:
            if red < 0 or red > 255:
                raise ColourError(7)
            if green < 0 or green > 255:
                raise ColourError(8)
            if blue < 0 or blue > 255:
                raise ColourError(9)
            return '\033[38;2;%i;%i;%im' % (red, green, blue)

    # Background:
    class bg(object):
        """Background Colours."""
        # 4 bit colour (16 Colours)
        black: Final[str] = '\033[40m'
        red: Final[str] = '\033[41m'
        green: Final[str] = '\033[42m'
        orange: Final[str] = '\033[43m'
        blue: Final[str] = '\033[44m'
        purple: Final[str] = '\033[45m'
        cyan: Final[str] = '\033[46m'
        light_grey: Final[str] = '\033[47m'
        dark_grey: Final[str] = '\033[100m'
        light_red: Final[str] = '\033[101m'
        light_green: Final[str] = '\033[102m'
        yellow: Final[str] = '\033[103m'
        lightblue: Final[str] = '\033[104m'
        pink: Final[str] = '\033[105m'
        light_cyan: Final[str] = '\033[106m'
        white: Final[str] = '\033[107m'

        # 8-bit background colour (255 Colours):
        @staticmethod
        def colour(value: int) -> str:
            """
            Get an 8-bit background colour.
            :param value : int, The colour number. 0-255.
            :raises ColourError : On type error or value error
            :returns: str, The colour string.
            """
            if not isinstance(value, int):
                raise ColourError(1)
            if value < 0 or value > 255:
                raise ColourError(6)
            return '\033[48;5;%im' % value

        # 16-bit background colour (65,536 Colours)
        @staticmethod
        def rgb(red: int, green: int, blue: int):
            """
            Get a 16-bit background colour.
            :param red: int, The red value (0-255).
            :param green: int, The green value (0-255).
            :param blue: int, The blue value (0-255).
            :raises ColourError: On type error or value error.
            :return: str, The 16-bit colour string.
            """
            # Type check:
            if not isinstance(red, int):
                raise ColourError(2)
            if not isinstance(green, int):
                raise ColourError(3)
            if not isinstance(blue, int):
                raise ColourError(4)
            # Value check:
            if red < 0 or red > 255:
                raise ColourError(7)
            if green < 0 or green > 255:
                raise ColourError(8)
            if blue < 0 or blue > 255:
                raise ColourError(9)
            return '\033[48;2;%i;%i;%im' % (red, green, blue)


if __name__ == '__main__':
    # 4 bit colour:
    print("4 bit colour test:")
    print(Colours.fg.red, "This", "is", Colours.bg.dark_grey, "a", Colours.strikeThrough, "test", Colours.reset, "\n")
    # 8 bit colour:
    print("8 bit colour test:")
    for i in range(256):
        colourString = Colours.fg.colour(i) + '%3i' % i
        if i == 0:
            colourString += Colours.bg.white
        else:
            colourString += Colours.bg.black
        print(colourString, end='')
        print(Colours.reset + ' ', end='')
        if not i % 20:
            print()
    print(Colours.reset)
    # 16 bit colour:
    print("16 bit colour test:")
    for i in range(0, 256):
        print(Colours.fg.rgb(i, 0, 0) + '\u2588', end='')
    print()
    for i in range(0, 256):
        print(Colours.fg.rgb(0, i, 0) + '\u2588', end='')
    print()
    for i in range(0, 256):
        print(Colours.fg.rgb(0, 0, i) + '\u2588', end='')
    print(Colours.reset)

    # Test colour validations:
    fourBitControlTest = Colours.reverse
    fourBitFgTest = Colours.fg.black
    fourBitBgTest = Colours.bg.black
    eightBitFgTest = Colours.fg.colour(0)
    eightBitBgTest = Colours.bg.colour(0)
    sixteenBitFgTest = Colours.fg.rgb(0, 0, 0)
    sixteenBitBgTest = Colours.bg.rgb(255, 255, 255)
    badColour = "bad_colour"
    print("Four bit validations:")
    print("CONTROL is_control:")
    print(Colours.is_control(fourBitControlTest))
    print("CONTROL is_four_bit:")
    print(Colours.is_four_bit(fourBitControlTest))
    print()
    print("FG is_colour:")
    print(Colours.is_colour(fourBitFgTest))
    print("FG is_foreground:")
    print(Colours.is_foreground(fourBitFgTest))
    print("FG is_background:")
    print(Colours.is_background(fourBitFgTest))
    print("FG is_control:")
    print(Colours.is_control(fourBitFgTest))
    print("FG is 8 bit:")
    print(Colours.is_eight_bit(fourBitFgTest))
    print()
    print("BG is_colour:")
    print(Colours.is_colour(fourBitBgTest))
    print("BG is_foreground:")
    print(Colours.is_foreground(fourBitBgTest))
    print("BG is_background:")
    print(Colours.is_background(fourBitBgTest))
    print("BG is 16 bit:")
    print(Colours.is_sixteen_bit(fourBitBgTest))
    print("BG is 4 bit:")
    print(Colours.is_four_bit(fourBitBgTest))
    print()

    print("Eight bit Tests:")
    print("FG is_colour:")
    print(Colours.is_colour(eightBitFgTest))
    print("FG is_foreground:")
    print(Colours.is_foreground(eightBitFgTest))
    print("FG is background:")
    print(Colours.is_background(eightBitFgTest))
    print("FG is 4 bit:")
    print(Colours.is_four_bit(eightBitFgTest))
    print()
    print("BG is_colour:")
    print(Colours.is_colour(eightBitBgTest))
    print("BG is_foreground:")
    print(Colours.is_foreground(eightBitBgTest))
    print("BG is_background:")
    print(Colours.is_background(eightBitBgTest))
    print("BG is 16 bit:")
    print(Colours.is_sixteen_bit(eightBitBgTest))
    print("BG is 8 bit:")
    print(Colours.is_eight_bit(eightBitBgTest))
    print()

    print("Sixteen bit tests:")
    print("FG is Colour:")
    print(Colours.is_colour(sixteenBitFgTest))
    print("FG is_foreground:")
    print(Colours.is_foreground(sixteenBitFgTest))
    print("FG is_background:")
    print(Colours.is_background(sixteenBitFgTest))
    print("FG is 4 Bit:")
    print(Colours.is_four_bit(sixteenBitFgTest))
    print()
    print("BG is_colour:")
    print(Colours.is_colour(sixteenBitBgTest))
    print("BG is_foreground:")
    print(Colours.is_foreground(sixteenBitBgTest))
    print("BG is_background:")
    print(Colours.is_background(sixteenBitBgTest))
    print("BG is 8 bit:")
    print(Colours.is_eight_bit(sixteenBitBgTest))
    print("BG is 16 bit:")
    print(Colours.is_sixteen_bit(sixteenBitBgTest))

    exit(0)
