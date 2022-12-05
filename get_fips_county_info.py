import urllib.request as urllib2
import lxml.html
from lxml import etree
import pandas as pd

c = urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_United_States_FIPS_codes_by_county')

tree = lxml.html.fromstring(c.read())
table = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]')[0]
county_fips_to_names = pd.read_html(etree.tostring(table))[0]
county_fips_to_names.to_csv('fips_county_info.csv')
