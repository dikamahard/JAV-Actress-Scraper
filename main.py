import requests
#from requests.exceptions import Timeout
from bs4 import BeautifulSoup

url2 = "https://webscraper.io/test-sites/e-commerce/allinone"

currentPage = 1
idolLinks = []


while(currentPage < 5):
    url = "https://www.javdatabase.com/idols/page/" + str(currentPage)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    idolCards = soup.findAll('div', class_='idol-thumb')

    for card in idolCards:
        link = card.find('a').attrs['href']
        idolLinks.append(link)

    currentPage += 1
    
#print(idolLinks)


with open ('link.txt', 'w') as f:
    for link in idolLinks:
        f.write("%s\n" % link)





