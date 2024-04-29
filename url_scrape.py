import requests
from timeit import default_timer as timer
from datetime import timedelta
#from requests.exceptions import Timeout
from bs4 import BeautifulSoup

fileName = 'error2.txt'

def main():
    # Initialize Data
    url = "https://www.javdatabase.com/idols/page/"
    startPage = 1
    lastPage = 20
    idolUrls = []
    currentPage = 1
    

    # Master Method (Scrap all then append)
    # Not Recomended because last page error handling still doesn't work
    # Use this if you EXACTLY now the last page!!!
    """try :
        idolUrls = extract_url_data(url, startPage, lastPage)
        append_urls_to_txt(idolUrls, fileName)
    except LastPageException as e:
        print(idolUrls)
        print(e)
    finally:
        print('Appending the rest of data...')"""
    

    # Chunk Method (Scrap per 1 by 1, then append per 10 pages)
    # Recomended for big data scrape and doesn't know the exact page quantity
    try:
        while (True):
            idolUrls += extract_url_data(url, currentPage, currentPage)
            print(idolUrls)

            if (currentPage % 10 == 0): # After 10 pages of scraping, append the data to txt
                print(currentPage)
                append_urls_to_txt(idolUrls, fileName)
                idolUrls = []
            
            currentPage += 1
    except LastPageException as e: # append the rest of data because of last page
        print ("Hasil exception")
        print(idolUrls)
        append_urls_to_txt(idolUrls, fileName)
        print (e)
    finally:
        print('Appending the rest of data...')


def append_urls_to_txt(urlList, filename):
   with open (filename, 'a') as f:
        for url in urlList:
            f.write("%s\n" % url)


def extract_url_data(url, startPage, lastPage): 
    start = timer()
    currentPage = startPage
    urlCounter = 0
    pageCounter = 0
    urlList = []

    while(currentPage <= lastPage):
        pageCounter += 1
        print('Scraping Page {}....'.format(currentPage))
        link = url + str(currentPage)
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        idolCards = soup.findAll('div', class_='idol-thumb')

        if(not idolCards):  # Throw exception last page then append the rest of data before exception to txt
            raise LastPageException('Last Page Has Been Reached!!!')


        for card in idolCards:
            urlCounter += 1
            link = card.find('a').attrs['href']
            urlList.append(link)

        currentPage += 1
    
    end = timer()
    print('Done scraping {} urls from {} pages'.format(urlCounter, pageCounter))
    print("Time's Taken : {}".format(timedelta(seconds=end-start)))
    return urlList


class LastPageException(Exception):
    pass


if __name__ == '__main__':
    main()