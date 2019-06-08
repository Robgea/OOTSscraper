from bs4 import BeautifulSoup
import requests
import os
import re
import sys

def comic_start():
    os.makedirs('oots', exist_ok = True)
    pagenum = 1


    baseurl = 'http://www.giantitp.com/'
    url = 'http://www.giantitp.com/comics/oots0001.html'
    while not url.endswith('#'):
        oots_comic = requests.get(url)
        oots_soup = BeautifulSoup(oots_comic.content, "html5lib")
        imgs = oots_soup.find_all('img',{'src':re.compile('/comics/images/.*')})
        if imgs == []:
            sys.stdout.write(f"Couldn't find comic number {pagenum}")
            sys.stdout.flush()
        else:
            comimg = imgs[0].get('src')
            comurl = f'{baseurl}{comimg}'
            comdown = requests.get(comurl)
            comend = comurl[-4:]
            comname = f'oots{str(pagenum).zfill(4)}{comend}'
            sys.stdout.write('\n')
            sys.stdout.write(f'Downloading comic number: {pagenum}')
            sys.stdout.flush()
            imageFile = open(os.path.join('oots', os.path.basename(comname)), 'wb')
            for chunk in comdown.iter_content(100_000):
                imageFile.write(chunk)
            imageFile.close()

        next_image =oots_soup.find(title = 'Next Comic')
        next_link = next_image.parent.get('href')
        url = f'{baseurl}{next_link}'
        pagenum += 1

    sys.stdout.write('\n All done!')
    sys.stdout.flush()


def main():
    comic_start()


if __name__ == '__main__':
    main()