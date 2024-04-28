import requests
import json 
#from requests.exceptions import Timeout
from bs4 import BeautifulSoup


url = "https://www.javdatabase.com/idols/maria-ozawa/"
# with open ('link.txt', 'r') as f:
#     urls = [line.strip() for line in f]

profile = {}
codeList = []
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

idolProfile = soup.find('div', class_= 'col-12 col-xxl-7 col-xl-7 col-lg-7 col-md-12 col-sm-12')
idolVideos = soup.find('div', class_= 'facetwp-template').find('div', class_='row')
idolPhoto = soup.find('div', class_= 'idol-portrait').find('img')['src']


def extract_data_profile(text):
    if (text == 'Measurements:'):
        return idolProfile.find('b', string=text).next_sibling.strip(" -")
    
    if (text == 'Shoe Size:'):
        return idolProfile.find('b', string=text).next_sibling.strip(" ")

    b_tag_result = idolProfile.find('b', string=text).find_next_sibling()
    if (b_tag_result.name == 'a'):   # has a link href, not unknown
        return b_tag_result.text
    else : 
        return 'Unknown'


def extract_data_videos():
    for video in idolVideos:
        code = video.find('a', class_='cut-text').text.strip(' ')
        codeList.append(code)


scrape = ['Age:', 'DOB:', 'Birthplace:', 'Sign:', 'Blood:', 'Measurements:', 'Cup:', 'Height:', 'Shoe Size:', 'Hair Length(s):', 'Hair Color(s):']
label = ['age', 'dob', 'birthplace', 'zodiac', 'blood', 'size3', 'cup', 'height', 'shoe', 'hairlength', 'haircolor']
profile['name'] = idolProfile.find('h1', class_='idol-name').text.strip(" - JAV Profile")
profile['img'] = idolPhoto

for i in range(0, 11):
    profile[label[i]] = extract_data_profile(scrape[i])

extract_data_videos()
profile['code'] = codeList
print(profile)


with open("result.json", "w") as f:
    json.dump(profile, f)


