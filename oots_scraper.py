from bs4 import BeautifulSoup
import requests
import os
import re
import sys
import shelve

def comic_start():
    os.makedirs('oots', exist_ok = True)
    oots_tracker = shelve.open('OOTS_tracker', writeback = True)
    baseurl = 'http://www.giantitp.com/'
    last_com = False


    if 'url' in oots_tracker:
        url = oots_tracker['url']
        pagenum = oots_tracker['pagenum']

        try:
            page = requests.get(url)
            oots_soup = BeautifulSoup(page.content, "html5lib")
            next_image = oots_soup.find(title = 'Next Comic')
            next_link = next_image.parent.get('href')
            if next_link.endswith('#'):
                sys.stdout.write('No new comics since this was last run!')
                sys.stdout.flush()
                last_com = True
                return 'Done!'

            else:
                sys.stdout.write('Continuing from last comic downloaded...\n')
                sys.stdout.flush()
                url = f'{baseurl}{next_link}'
        except:
            sys.stdout.write('Error connecting to the Order of the Stick server.\n')
            sys.stdout.flush()
            return 'ERROR!'

    else:
        pagenum = 1
        url = 'http://www.giantitp.com/comics/oots0001.html'



    while last_com == False:
        try:
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

            next_image = oots_soup.find(title = 'Next Comic')
            next_link = next_image.parent.get('href')

        except:
            sys.stdout.write(f'Error while downloading comic number {pagenum} at URL {url}. Saving progress and aborting.\n')
            sys.stdout.flush()
            oots_tracker['url'] = old_url
            oots_tracker['pagenum'] = pagenum
            oots_tracker.close()
            return 'ERROR!'



        if next_link.endswith('#'):
            sys.stdout.write('All done!')
            sys.stdout.flush()
            oots_tracker['url'] = url
            oots_tracker['pagenum'] = pagenum
            oots_tracker.close()
            last_com = True


        else:
            old_url = url    
            url = f'{baseurl}{next_link}'
            pagenum += 1



def main():
    comic_start()

if __name__ == '__main__':
    main()