import pandas as pd

# Scrape Choice Inline Schedule and print results as a table
# tables = pd.read_html("http://www.choiceinline.com/stats#/319/schedule?division_id=3508")
tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F")

print(tables[0])