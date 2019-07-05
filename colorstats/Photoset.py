from .Photo import Photo
from math import sqrt
from itertools import combinations
from statistics import mean, stdev


class Photoset:
    """Class to perform likeness calculations on multiple Photo objects."""

    def __init__(self, photolist: []):
        """Constructor

        Parameters:
        photolist ([]): list containing 2 or more Photo objects

        """

        self.__saturation_likeness = None
        self.__overall_likeness = None
        self.__lightness_likeness = None
        self.__color_likeness = None
        self.__fraction_likeness = None
        self.__avg_lightness = None
        self.__avg_saturation = None

        if len(photolist) < 2:
            raise ValueError("Length of input photo list must be at least 2.")
        for item in photolist:
            if type(item) != Photo:
                raise TypeError("Non-Photo object found in input list")
        self.photolist = photolist
        self.filenames_index = {}
        for photo in photolist:
            self.filenames_index[photo.filename] = photolist.index(photo)
        self.length = len(photolist)

    @staticmethod
    def __color_difference(col1, col2):
        sum_of_sq = 0
        for i in range(3):
            sum_of_sq += (col1[i] - col2[i]) ** 2
        return sqrt(sum_of_sq) / (sqrt(3 * (255 ** 2)))

    def __get_avg_rgb(self):
        averages = {}
        colorlist = ['black', 'blue', 'cyan', 'dark grey', 'green', 'grey', 'light grey', 'magenta', 'orange',
                     'red', 'turquois', 'violet', 'white', 'yellow']
        for color in colorlist:
            averages[color] = []
        for photo in self.photolist:
            for color in photo.get_color_data():
                averages[color].append(photo.get_color_data()[color]['RGB'])
        for color in averages:
            while len(averages[color]) < self.length:
                averages[color].append((0, 0, 0))  # accounts for photos lacking a specific color
        return averages

    def __get_fraction_rgb(self):
        fractions = {}
        colorlist = ['black', 'blue', 'cyan', 'dark grey', 'green', 'grey', 'light grey', 'magenta', 'orange',
                     'red', 'turquois', 'violet', 'white', 'yellow']
        for color in colorlist:
            fractions[color] = []
        for photo in self.photolist:
            for color in photo.get_color_data():
                fractions[color].append(round(photo.get_color_data()[color]['%'], 2))
        for color in fractions:
            while len(fractions[color]) < self.length:
                fractions[color].append(0)
        return fractions

    def get_color_likeness(self):
        """Get the likeness of Photo objects in terms of color shades."""

        if self.__color_likeness is not None:
            return self.__color_likeness

        data = self.__get_avg_rgb()
        running_sum = 0
        for color in data:
            differences = [self.__color_difference(c1, c2) for c1, c2 in combinations(data[color], 2)]
            running_sum += sum(differences) / len(differences)
        x = running_sum / len(data)
        self.__color_likeness = round(1 - abs((1 / (1 + 2.7 ** (-4 * x)) - .5)) * 2, 4)
        return self.__color_likeness

    def get_fraction_likeness(self):
        """Get the likeness of Photo objects in terms of fractional makeup of colors."""

        if self.__fraction_likeness is not None:
            return self.__fraction_likeness

        data = self.__get_fraction_rgb()
        running_sum = 0
        for color in data:
            differences = [abs(p1 - p2) for p1, p2 in combinations(data[color], 2)]
            running_sum += sum(differences) / len(differences)
        x = running_sum / len(data)
        self.__fraction_likeness = round(1 - abs((1 / (1 + 2.7 ** (-20 * x)) - .5)) * 2, 4)
        return self.__fraction_likeness

    def get_lightness_likeness(self):
        """Get the likeness of Photo objects in terms of lightness."""

        if self.__lightness_likeness is not None:
            return self.__lightness_likeness

        lightness_list = []
        for photo in self.photolist:
            lightness_list.append(photo.get_average_lightness())
        differences = [abs(x - y) for x, y in combinations(lightness_list, 2)]
        self.__lightness_likeness = round(1 - sum(differences) / len(differences), 4)
        return self.__lightness_likeness

    def get_saturation_likeness(self):
        """Get the likeness of Photo objects in terms of saturation."""

        if self.__saturation_likeness is not None:
            return self.__saturation_likeness

        saturation_list = []
        for photo in self.photolist:
            saturation_list.append(photo.get_average_saturation())
        differences = [abs(x - y) for x, y in combinations(saturation_list, 2)]
        self.__saturation_likeness = round(1 - sum(differences) / len(differences), 4)
        return self.__saturation_likeness

    def get_overall_likeness(self, color_weight=.25, fraction_weight=.25, lightness_wieght=.25,
                             saturation_weight=.25):
        """Get the likeness of Photo objects overall.

        Calculates overall likeness using a weighted sum of color, fraction, lightness, and saturation likeness values.

        Parameters:
        color_weight (float): weight attributed to color
        fraction_weight (float): weight attributed to fractional color makeup
        lightness_weight (float): weight attributed to lightness
        saturation_weight (float): weight attributed to saturation

        """

        if self.__overall_likeness is not None:
            return self.__overall_likeness

        if color_weight + fraction_weight + saturation_weight + lightness_wieght != 1.0:
            raise ValueError("Wieghts must add up to 1.")

        self.__overall_likeness = round(
            color_weight * self.get_color_likeness() + fraction_weight * self.get_fraction_likeness() +
            lightness_wieght * self.get_lightness_likeness() +
            saturation_weight * self.get_saturation_likeness(), 4)
        return self.__overall_likeness

    def get_avg_lightness(self):
        """Get the average lightness of photos in a Photoset."""

        if self.__avg_lightness is not None:
            return self.__avg_lightness

        lightnesses = []
        for p in self.photolist:
            lightnesses.append(p.get_average_lightness())
        self.__avg_lightness = mean(lightnesses)
        return self.__avg_lightness

    def get_std_lightness(self):
        """Get the standard deviation of lightness of photos in a Photoset."""

        lightnesses = []
        for p in self.photolist:
            lightnesses.append(p.get_average_lightness())
        return stdev(lightnesses)

    def get_avg_saturation(self):
        """Get the average saturation of photos in a Photoset."""

        if self.__avg_saturation is not None:
            return self.__avg_saturation

        saturations = []
        for p in self.photolist:
            saturations.append(p.get_average_saturation())
        self.__avg_saturation = mean(saturations)
        return self.__avg_saturation

    def get_std_saturation(self):
        """Get the standard deviation of saturation of photos in a Photoset."""

        saturations = []
        for p in self.photolist:
            saturations.append(p.get_average_saturation())
        return stdev(saturations)
