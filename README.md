![python](https://img.shields.io/badge/python-v.3.9-blue) [![license](https://img.shields.io/github/license/juliaszulc/mouline_converter)](https://github.com/JuliaSzulc/mouline_converter/blob/main/LICENSE.md)

[![tests](https://img.shields.io/github/workflow/status/juliaszulc/mouline_converter/tests?label=tests)](https://github.com/JuliaSzulc/mouline_converter/actions/workflows/tests.yml) <!-- [START BADGES] -->
<!-- [END BADGES] -->

[![flake8](https://img.shields.io/github/workflow/status/juliaszulc/mouline_converter/flake8?label=flake8)](https://github.com/JuliaSzulc/mouline_converter/actions/workflows/flake8.yml)
[![black](https://img.shields.io/github/workflow/status/juliaszulc/mouline_converter/black?label=black)](https://github.com/JuliaSzulc/mouline_converter/actions/workflows/black.yaml)

![Heroku](https://pyheroku-badge.herokuapp.com/?app=mouline-converter&style=flat)  

### TL;DR quickstart
- **USER MODE** - run the app and notebooks:
`pip install -e ".[user]"`
- **DEV MODE** - install all dependencies:
`pip install -e ".[dev]"`

# [WORK IN PROGRESS] Mouline Converter
[Abstract - TODO]

## Glossary
* **mouline**/**floss** - cotton thread commonly used in hand embroidery
* **DMC** - the most common brand producing textiles, threads, embroidery/sewing accessories etc.
* **Ariadna** - polish thread producer; as far as I know, not common outside Poland and Eastern Europe
* **mouline color/number** - each color is identified by a number (sometimes with some letters added or, in case of special colors, by letters only) that is not standardized outside a specific brand in any way
* **swatch** - a sample or set of samples of colors shown in order to present and compare them

## Motivation
The majority of patterns available use DMC color codes since it's the most popular brand worldwide. The majority of my floss collection are from Ariadna (I find the quality comparable to DMC and the price is better). Converting color codes always takes some time and it's not trivial for a few reasons:
1. DMC offers much more colors than Ariadna
2. Ariadna is pretty much unknown outside Poland and there are no official conversion charts. The unofficial ones are not always reliable
3. There are no 1:1 substitutes and so, for example, the most similar Ariadna colors that could substitute for some DMC red are hues that are more orange or more pink. The choice would depend on a specific pattern and other chosen colors (it can be very crucial with shading).

## Goal
I wanted to make a tool finding the closest Ariadna substitutes to a given DMC color code. It was important that there was a possibility to display the colors and be able to compare them in order to choose the most fitting one.

## Implementation
### 1. Creating lists with all DMC and Ariadna mouline available including color identifiers and hexadecimal color codes
[TODO]
### 2. Implementing swatching of colors in order to visualize compare them easily
[TODO]
### 2. Testing different colors differences formulas
[TODO]

___
## Notes
* I found myself very confused about Lab/CIELAB/CIEL\*a\*b\* etc. and, though I acknowledge that these are not supposed to be used interchangeably, these might be mixed up in this project so feel free to point out my errors.
## Sources
* [*Color difference* - Wikipedia](https://en.wikipedia.org/wiki/Color_difference)
* [*CIELAB color space* - Wikipedia](https://en.wikipedia.org/wiki/CIELAB_color_space)
* [Bruce Lindbloom's website](http://www.brucelindbloom.com/)
* [*Completely Painless Programmer's Guide to XYZ, RGB, ICC, xyY, and TRCs* - Elle Stone](https://ninedegreesbelow.com/photography/xyz-rgb.html)
* [*Delta E 101* - Zachary Schuessler](https://zschuessler.github.io/DeltaE/learn/)
