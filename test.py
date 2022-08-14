from bs4 import BeautifulSoup

html = open("test.html", "r").read()
# print(html)
bs = BeautifulSoup(html, features="html.parser")
search_results = bs.select("#latest_release .group")
print(len(search_results))

