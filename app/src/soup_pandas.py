import requests
from bs4 import BeautifulSoup #pip install bs4
import pandas

url = 'https://www.worldometers.info/gdp/gdp-by-country/'
load_web_page = requests.get(url)
soup_page_parser = BeautifulSoup(load_web_page.content, 'html.parser')
target_table = soup_page_parser.find("table", {"class": "datatable"})
data_frame = pandas.read_html(str(target_table))[0] #extract from first table found with that name
print(data_frame.head(5))

data_frame.to_excel("web_table_results.xlsx")