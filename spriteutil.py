# -*- coding: utf-8 -*-
from statistics import mode


def find_most_common_color(image):
    '''Get pixel that is the most used in image.

    The data type of the value returned depends on the image's mode:
        - an integer if the mode is grayscale;
        - a tuple (red, green, blue) of integers if the mode is RGB;
        - a tuple (red, green, blue, alpha) of integers if the mode is RGBA.

    Parameter
    ----------
    param : PIL.Image Object

    Returns
    -------
    tupple
        Value of pixel that is the most used in image.
    '''
    list_pixels = []
    for x in range(image.size[0]):
        list_pixels += [image.getpixel((x, y)) for y in range(image.size[1])]
    return mode(list_pixels)


class Sprite():
    def __init__(self, label=None, x1=None, y1=None,x2=None, y2=None):
        """Constructor"""

        def check_value(*list_values):
            """Assure valid argument.

            The valid argument is positive integer.
            Raise ValueError if there are invalid argument.
            """
            invalid = False
            error_message = "Invalid coordinates"
            for element in list_values:
                if ("-" in str(element)) or (type(element) != int):
                    raise ValueError(error_message)
            if (x2 < x1) or (y2 < y1):
                raise ValueError(error_message)

        check_value(label, x1, y1, x2, y2)
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__lable = label
        self.__top_left = (self.__x1, self.__y1)
        self.__bottom_right = (self.__x2, self.__y2)

    @property
    def label(self):
        """return value of self.__label"""
        return self.__label

    @property
    def top_left(self):
        """return value of self.__top_left"""
        return self.__top_left

    @property
    def width(self):
        """return image's width"""
        return (self.__x2 - self.__x1 + 1)
    
    @property
    def height(self):
        """return image's height"""
        return (self.__y2 - self.__y1 + 1)

    # @property
    # def duration(self):
    #     """return value of self.__duration"""
    #     return self.__duration
    #
    # @property
    # def episode_id(self):
    #     """return value of self.__episode_id"""
    #     return self.__episode_id
    #
    # @staticmethod
    # def __parse_episode_id(url):
    #     """Find episode identifier.
    #
    #     """
    #     return url[(url.find("images/") + 7):(len(url) - 4)]
