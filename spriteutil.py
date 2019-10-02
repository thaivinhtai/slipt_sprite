# -*- coding: utf-8 -*-
from statistics import mode
from PIL import Image


def __process_data_from_check_neighbor(label_map, x, y,
                                       check_dict, label, existed_labels,
                                       check, list_labeled, assigned_label):
    if check and label_map[x][y] == -1:
        label_map[x][y] = assigned_label
        check_dict[assigned_label] += list_labeled
    elif label_map[x][y] == -1:
        label_map[x][y] = label
        label += 1
        check_dict[label] = []
        existed_labels.append(label)
    return label_map, check_dict, label, existed_labels


def __check_neighborhood(label_map, current_coordinates, existed_labels):
    '''Look around a pixel's neighbor.

    This function browses all pixels that surrounding the input pixel.
    The process will go through from the upper-left pixel and check if the
    inputed pixel is near the valid labeled pixel or not.

    Parameter
    ----------
    label_map : nested list
        A two dimensions array that marks wich pixel is foreground or not.
    current_coordinates : tupple
        The coordinates of the base pixel.
    existed_labels : list
        A number that marks the current blod.

    Returns
    -------
    bool
        - true if the inputed pixel is near the valid labeled pixel
    list
        - list valid label near inputed pixel
    int
        - the label assigns to inputed pixel
    '''
    x = current_coordinates[0]
    y = current_coordinates[1]
    list_labeled = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
    for direction in directions:
        x_neighbor = x + direction[0]
        y_neighbor = y + direction[1]
        try:
            if label_map[x_neighbor][y_neighbor] in existed_labels:
                list_labeled.append(label_map[x_neighbor][y_neighbor])
        except IndexError:
            pass
    if list_labeled:
        return True, list_labeled, list_labeled[0]
    return False, None, None


def find_most_common_color(image):
    '''Get pixel that is the most used in image.

    The data type of the value returned depends on the image's mode:
        - an integer if the mode is grayscale;
        - a tuple (red, green, blue) of integers if the mode is RGB;
        - a tuple (red, green, blue, alpha) of integers if the mode is RGBA.

    Parameter
    ----------
    image : PIL.Image Object

    Returns
    -------
    tupple
        Value of pixel that is the most used in image.
    '''
    list_pixels = []
    for x in range(image.size[0]):
        list_pixels += [image.getpixel((x, y)) for y in range(image.size[1])]
    return mode(list_pixels)


def find_sprites(image, background_color=None):
    ''' Isolate each sprite, producing bounding boxes.

    This function isolates each sprite, producing bounding boxes with correct
    sizes and identifying isolated parts of a sprite as an included segment.

    This function accepts an optional argument background_color (an integer if
    the image format is grayscale, or a tuple (red, green, blue) if the image
    format is RGB) that identifies the background color (i.e., transparent
    color) of the image. The function ignores any pixels of the image with this
    color.

    If this argument background_color is not passed, the function determines
    the background color of the image as follows:

        - The image, such as a PNG file, has an alpha channel: the function
        ignores all the pixels of the image which alpha component is 255;

        - The image has no alpha channel: the function identifies the most
        common color of the image as the background color (cf. our function
        find_most_common_color).

    The function returns a tuple (sprites, label_map) where:

        - sprites: A collection of key-value pairs (a dictionary) where each
        key-value pair maps the key (the label of a sprite) to its associated
        value (a Sprite object);

        - label_map: A 2D array of integers of equal dimension (width and
        height) as the original image where the sprites are packed in. The
        label_map array maps each pixel of the image passed to the function to
        the label of the sprite this pixel corresponds to, or 0 if this pixel
        doesn't belong to a sprite (e.g., background color).

    Parameter
    ----------
    image : PIL.Image Object

    background_color : optional
        - an integer if the image format is grayscale
        - a tuple (red, green, blue) if the image format is RGB

    Returns
    -------
    tupple
        (sprites, label_map)
    '''

    def get_label_map(image, index1=-1, index2=0, slice1=3, slice2=4,
                      background_color=(0, 0, 0, 255)):
        '''Get label_map.

        Parameter
        ----------
        image : PIL.Image Object
        index1 : int
            value be added to label_map, 1 is foreground, 0 is backgroup
                - image.mode == RGBA, index1 = -1
                - otherwise, index1 = 0
        index2 : int
            value be added to label_map, 1 is foreground, 0 is backgroup
                - image.mode == RGBA, index2 = 0
                - otherwise, index2 = -1
        slice1 : int
            -   slice1 = 3 if image.mode == RGBA
            -   otherwise, slice1 = 0
        slice2 : int
            -   slice1 = 4 if image.mode == RGBA
            -   otherwise, slice2 = None
        background_color : tupple
            Background color

        Returns
        -------
        list
            label_map
        '''
        label_map = []
        for y in range(image.size[1]):
            label_map.append([])
            for x in range(image.size[0]):
                if image.getpixel((x, y))[slice1:slice2] ==\
                    background_color[slice1:slice2]:
                    label_map[y].append(index1)
                else:
                    label_map[y].append(index2)
        return label_map

    if not background_color:
        background_color = find_most_common_color(image)
    label_map = []
    if image.mode == 'RGBA':
        label_map = get_label_map(image)
    else:
        label_map = get_label_map(image, index1=0, index2=-1,
                                  slice1=0, slice2=None,
                                  background_color=background_color)

    label = 1
    dict_related_label = {1: []}
    existed_labels = [label]
    for x in range(len(label_map)):
        for y in range(len(label_map[0])):
            label_map, dict_related_label, label, existed_labels =\
                __process_data_from_check_neighbor\
                    (label_map, x, y, dict_related_label,
                     label, existed_labels,
                     *__check_neighborhood(label_map, (x, y), existed_labels))
    for key, value in dict_related_label.items():
        dict_related_label[key] = set(value)

    print(dict_related_label)
    for key in existed_labels:
        stop_flag = 0
        while True:
            try:
                key_to_be_del = set(dict_related_label[key])
                if key_to_be_del == stop_flag:
                    False
                for element in key_to_be_del:
                    [dict_related_label[key].add(value)
                     for value in dict_related_label[element]]
                for element in key_to_be_del:
                    if element != key:
                        del dict_related_label[element]
                stop_flag = set(key_to_be_del)
            except KeyError:
                pass
    print(dict_related_label)




    return label_map


class Sprite():
    def __init__(self, label=None, x1=None, y1=None, x2=None, y2=None):
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


if __name__ == '__main__':
    image = Image.open('metal_slug_sprite_large.png')
    print(find_most_common_color(image))
    print(*find_sprites(image), sep='\n')
