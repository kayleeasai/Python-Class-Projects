import requests
from bs4 import BeautifulSoup
import os
import pprint

res = requests.get('https://www.gocomics.com/pearlsbeforeswine/')
res.raise_for_status()
soup = BeautifulSoup(res.text)

#click read more
read_more = soup.select('div:is(.gc-deck--cta-0)')
# print(len(read_more))
# pprint.pprint(vars(read_more[0]))

def save_image(n):
    # find read more url
    read_more_url = 'http://www.gocomics.com' + read_more[0].contents[1].attrs['href']
    read_more_res = requests.get(read_more_url)
    read_more_res.raise_for_status()
    soup = BeautifulSoup(read_more_res.text)
    for x in range(n):
    # find image tag
        comic_div = soup.select('picture:is(.item-comic-image)')
        # print(comic_div)
        # print(len(comic_div))
        # pprint.pprint(vars(comic_div[0]))

    # find image url
        image_url = comic_div[0].contents[0].attrs['src']
        image_res = requests.get(image_url)
        image_res.raise_for_status()
        print(image_url)

    # save image url
        image_file = open(os.path.basename(image_url), 'wb')
        for chunk in image_res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()

    #get prev url
        prev_link = soup.select('a:is(.fa-caret-left)')
        url = 'https://www.gocomics.com/' + prev_link[0].attrs['href']
        url_res = requests.get(url)
        soup = BeautifulSoup(url_res.text)
        print(soup)


save_image(10)
