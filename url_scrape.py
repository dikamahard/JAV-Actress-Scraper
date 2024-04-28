import requests
from timeit import default_timer as timer
from datetime import timedelta
#from requests.exceptions import Timeout
from bs4 import BeautifulSoup


def main():
    # Initialize Data
    url = "https://www.javdatabase.com/idols/page/"
    startPage = 1
    lastPage = 10
    idolUrls = []

    idolUrls = extract_url_data(url, startPage, lastPage)
    url_to_txt(idolUrls, 'urls.txt')


def url_to_txt(urlList, filename):
   with open (filename, 'a') as f:
        for url in urlList:
            f.write("%s\n" % url)


def extract_url_data(url, startPage, lastPage): 
    start = timer()
    currentPage = startPage
    index = 0
    urlList = []

    while(currentPage <= lastPage):
        print('Scraping Page {}....'.format(currentPage))
        link = url + str(currentPage)
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        idolCards = soup.findAll('div', class_='idol-thumb')

        for card in idolCards:
            index += 1
            link = card.find('a').attrs['href']
            urlList.append(link)

        currentPage += 1
    
    end = timer()
    print('Done scraping {} urls from {} pages'.format(index, currentPage-1))
    print("Time's Taken : {}".format(timedelta(seconds=end-start)))
    return urlList


if __name__ == '__main__':
    main()