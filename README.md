# ColorStats

Python package for processing color data from images.

### Installation
Install colorstats with:
```commandline
pip3 install colorstats
```

### Overview
ColorStats allows users to process pixel data from images in order to 
determine various statistics/attributes of the color composition of images.
It also allows users to determine the similarity of a set of images 
using these statistics.

### Functionality/Features

##### Single Image 

- generate the average shade of each general color (red, blue, etc. )
present in an image and their standard deviations
- calculate average saturation and lightness
- calculate the percentage color composition of the image


##### Sets of Images

- calculate average and standard deviation of saturation and lightness across all images
- calculate similarity based on:
    1. average shades of colors
    2. percentage color composition
    3. average saturation and lightness
    4. weighted some of the above values
    

