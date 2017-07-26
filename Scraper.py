from lxml import html
import requests
import itertools
import re

# # #
# A python script which scrapes Wikipedia's list of colors for the names and hex codes of each of the 1400+ colors
# on the webpage.
#
# Each entry in the final list `colors` should correspond to the same index entry in `hexes`
#
# Any time this is edited, it should be readded to the ColorPalette Android project
#
# Michael Crinite 07/11/2017
# # #

# Wikipedia List of colors: A-F
page = requests.get('https://en.wikipedia.org/wiki/List_of_colors:_A-F')
tree = html.fromstring(page.content)

colors_a_f_a = tree.xpath('//table[@class="wikitable sortable"]/tr/th/a/text()')
colors_a_f_th = tree.xpath('//table[@class="wikitable sortable"]/tr/th/text()')
hex_a_f = tree.xpath('//table[@class="wikitable sortable"]/tr/td[1]/text()')

# Wikipedia List of colors: G-M
page = requests.get('https://en.wikipedia.org/wiki/List_of_colors:_G-M')
tree = html.fromstring(page.content)

colors_g_m_a = tree.xpath('//table[@class="wikitable sortable"]/tr/th/a/text()')
colors_g_m_th = tree.xpath('//table[@class="wikitable sortable"]/tr/th/text()')
hex_g_m = tree.xpath('//table[@class="wikitable sortable"]/tr/td[1]/text()')

# Wikipedia List of colors: N-Z
page = requests.get('https://en.wikipedia.org/wiki/List_of_colors:_N-Z')
tree = html.fromstring(page.content)

colors_n_z_a = tree.xpath('//table[@class="wikitable sortable"]/tr/th/a/text()')
colors_n_z_th = tree.xpath('//table[@class="wikitable sortable"]/tr/th/text()')
hex_n_z = tree.xpath('//table[@class="wikitable sortable"]/tr/td[1]/text()')

# Consolidate the a and th fields into one list
# Because "St. Patrick's blue" messes up the sorting we have to fix it first
index_of_pat = colors_n_z_a.index("St. Patrick's blue")
colors_n_z_a[index_of_pat] = "Saint Patrick's Blue"

# Now we can continue
# First things first, we need to remove all non-alphanumeric characters from each string
pattern = re.compile('([^\s\w]|_)+')
messy_list = [pattern.sub('', x.lower()) for x in
              itertools.chain(colors_a_f_a[9:], colors_a_f_th[10:], colors_g_m_a[9:],
                              colors_g_m_th[10:], colors_n_z_a[9:], colors_n_z_th[10:])]
# Now we can sort our list
sorted_list = sorted(messy_list)

hexes = list(itertools.chain(hex_a_f, hex_g_m, hex_n_z))
colors = []

# For some reason, Wikipedia writers decided to put only half of whatever "tawny" is from in the <a> tag
# Consequently, we have to leave it out or else we will have too many entries in the colors list
for x in sorted_list:
    if x != '\n' \
            and x != 'Hex' \
            and x != 'Hue' \
            and x != 'Satur.' \
            and x != 'Light' \
            and x != 'Value' \
            and x != ' tawny' \
            and not x.startswith('('):
        colors.append(x)

print("Colors ", len(colors), ": ", colors)
print("Hex Codes ", len(hexes), ": ", hexes)

with open("out.txt", 'w') as f2:
    # print("{", file=f2)
    for i, x in enumerate(colors):
        print(colors[i], ":", hexes[i], file=f2)
        # print("}", file=f2)
