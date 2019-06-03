from bs4 import BeautifulSoup
import requests
import os
import re
import sys



def comic_start():
    os.makedirs('oots', exist_ok = True)

    urlnum = 1

    while urlnum < 1166:
        url = f'http://www.giantitp.com/comics/oots{str(urlnum).zfill(4)}.html'
        oots_comic = requests.get(url)
        oots_soup = BeautifulSoup(oots_comic.content, "html5lib")
        imgs = oots_soup.find_all('img',{'src':re.compile('/comics/images/.*')})
        if imgs == []:
            print(f"Couldn't find comic number {urlnum}")
        else:
            comimg = imgs[0].get('src')
            comurl = f'http://www.giantitp.com/{comimg}'
            comdown = requests.get(comurl)
            comend = comurl[-4:]
            comname = f'oots{str(urlnum).zfill(4)}{comend}'
            sys.stdout.write('\n')
            sys.stdout.write(f'Downloading comic number: {urlnum}')
            sys.stdout.flush()
            imageFile = open(os.path.join('oots', os.path.basename(comname)), 'wb')
            for chunk in comdown.iter_content(100_000):
                imageFile.write(chunk)
            imageFile.close()



        urlnum += 1

# open OOTS page

# find latest comic

# download it


# go to end goal

comic_start()

'''print(str(4).zfill(4))
print(str(40).zfill(4))
print(str(400).zfill(4))
print(str(4000).zfill(4))'''