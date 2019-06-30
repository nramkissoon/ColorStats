from colorsys import rgb_to_hls
from PIL import Image
from math import sqrt
from collections import Counter
from statistics import stdev, median, StatisticsError


class Photo:
    """Class that stores color data for a specific photo."""

    def __init__(self, filename, pixel_count=30000):
        """Constructor.

        Parameters:
        filename (String): path to photo file
        pixel_count (int): number of pixels that should be loaded to be used by class

        """
        self.filename = filename
        self.im = Image.open(filename)
        self.im = self.im.resize([int(self.__resize_scale(self.im.size, float(pixel_count)) * s) for s in self.im.size],
                                 Image.ANTIALIAS)
        self.pixel_data = list(self.im.getdata())
        self.num_pixels = len(self.pixel_data)
        self.__color_stats = {}
        self.__color_data = self.__get_average_shades(self.__sort_colors(self.pixel_data))

    @staticmethod
    def __average_shade(pixel_list):
        if len(pixel_list) == 0:
            return None
        r, g, b = 0, 0, 0
        for pixel in pixel_list:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
        return round(r / len(pixel_list)), round(g / len(pixel_list)), round(b / len(pixel_list))

    @staticmethod
    def __resize_scale(size, pixels):
        x, y = size
        return sqrt(pixels / (x * y))

    @staticmethod
    def __rgb_to_hsl(r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0  # normalize rgb values
        h, l, s = rgb_to_hls(r, g, b)
        return h * 360.0, s, l

    def __color_classifier(self, tup):
        r, g, b = tup
        h, s, l = self.__rgb_to_hsl(r, g, b)
        if s >= .15:
            if 0 <= h < 40:
                return 'orange'
            elif 40 <= h < 80:
                return 'yellow'
            elif 80 <= h < 120:
                return 'green'
            elif 120 <= h < 160:
                return 'turquois'
            elif 160 <= h < 200:
                return 'cyan'
            elif 200 <= h < 240:
                return 'blue'
            elif 240 <= h < 280:
                return 'violet'
            elif 280 <= h < 320:
                return 'magenta'
            elif 320 <= h <= 360:
                return 'red'
        else:
            grey_cutoffs = [0.0, .25, .50, .75, 1.0]
            distances = []
            for val in grey_cutoffs:
                distances.append(abs(l - val))
            closest = grey_cutoffs[distances.index(min(distances))]
            if closest == 0.0:
                return "black"
            elif closest == .25:
                return "dark grey"
            elif closest == .50:
                return "grey"
            elif closest == .75:
                return "light grey"
            elif closest == 1.0:
                return "white"

    def __sort_colors(self, pixel_list):
        color_dict = {'red': [], 'orange': [], 'yellow': [],
                      'green': [], 'turquois': [], 'cyan': [],
                      'magenta': [], 'blue': [], 'violet': [],
                      'black': [], 'dark grey': [], 'grey': [],
                      'light grey': [], 'white': []}
        for pixel in pixel_list:
            color = self.__color_classifier(pixel)
            color_dict[color].append(pixel)
        for color in color_dict:
            avg = self.__average_shade(color_dict[color])
            self.__color_stats[color] = {}
            self.__color_stats[color]["mean"] = avg
            r = []
            g = []
            b = []
            for pixel in color_dict[color]:
                for i in range(3):
                    if i == 0:
                        r.append(pixel[i])
                    elif i == 1:
                        g.append(pixel[i])
                    else:
                        b.append(pixel[i])
            try:
                self.__color_stats[color]["median"] = (median(r), median(g), median(b))
                self.__color_stats[color]["stdev"] = (round(stdev(r), 2), round(stdev(g), 2), round(stdev(b), 2))
            except StatisticsError:
                self.__color_stats[color]["stdev"] = None
                self.__color_stats[color]["median"] = None
        return color_dict

    def __get_average_shades(self, color_dict):
        ret_dict = {}
        for color in color_dict:
            avg_shade = self.__average_shade(color_dict[color])
            if avg_shade:  # some colors are not present in an image so the avg_shade is None
                ret_dict[color] = {}
                ret_dict[color] = {'RGB': avg_shade, 'HEX': '#%02x%02x%02x' % avg_shade,
                                   '%': round(len(color_dict[color]) / self.num_pixels, 4)}
        return ret_dict

    def get_n_most_common_colors(self, n):
        """Get the 'n' most common colors in the Photo.

        Returns:
        dictionary of most common colors and their respective RGB, HEX, and percentage makeup values.
        """
        l = {}
        for color in self.__color_data:
            l[color] = self.__color_data[color]['%']
        count_dict = Counter(l)
        l = {}
        for color in count_dict.most_common(n):
            l[color[0]] = self.__color_data[color[0]]
        return l

    def get_average_lightness(self):
        """Get the average lightness of Photo.

        Returns:
        int: average of lightness of pixels using l value in HSL.
        """
        running_sum = 0
        for pixel in self.pixel_data:
            hsl = self.__rgb_to_hsl(pixel[0], pixel[1], pixel[2])
            running_sum += hsl[2]
        return running_sum / self.num_pixels

    def get_average_saturation(self):
        """Get the average saturation of Photo.

        Returns:
        int: average of saturation of pixels using s value in HSL.
        """
        running_sum = 0
        for pixel in self.pixel_data:
            hsl = self.__rgb_to_hsl(pixel[0], pixel[1], pixel[2])
            running_sum += hsl[1]
        return running_sum / self.num_pixels

    def get_color_data(self, colors: [str] = None):
        """Get color data of a Photo.

        Parameters:
        colors [str]: list of colors to be included in the returned data
        """

        if colors is None or colors == []:
            return self.__color_data
        return_data = {}
        for color in colors:
            try:
                return_data[color] = self.__color_data[color]
            except KeyError:
                pass
        return return_data

    def get_color_stats(self, colors: [str] = None):
        """Get color stats of a Photo.

        Parameters:
        colors [str]: list of colors to be included in the returned data

        Returns:
        return_data {}: contains mean shade of color, standard deviation and median of rgb components
        """

        if colors is None or colors == []:
            return self.__color_stats
        return_data = {}
        for color in colors:
            try:
                return_data[color] = self.__color_stats[color]
            except KeyError:
                pass
        return return_data
