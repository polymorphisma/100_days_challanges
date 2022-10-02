from os.path import join
import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import etree


class Downloader:
    def __init__(self, manga_name, manga_url, download_loc):
        self.main_url = 'https://mangapill.com'
        self.manga_name = manga_name
        self.manga_url = manga_url
        self.download_loc = download_loc
    
    def requesting_soup(url):
        response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser') 
    
    @staticmethod
    def making_url(lists):
        url = 'https://mangapill.com/search?q=' + '+'.join(lists) 
        return url
        

    @staticmethod
    def manga_options(manga):
        
        dicts = {
            
        }
        manga_name_list = manga.lower().split(' ')
        url = Downloader.making_url(manga_name_list)

        soup = Downloader.requesting_soup(url)
        dom = etree.HTML(str(soup))
        
        value = dom.xpath('/html/body/div[1]/div[3]')

        for i in value:
            for index, div in enumerate(i.findall('div')):
                key_text = div.xpath(f'/html/body/div[1]/div[3]/div[{index + 1}]/div/a/div')[0].text
                value_url = div.findall('a')
                
                dicts[key_text] = value_url[0].get("href")

        return dicts

    def download(self):
        url = self.main_url + self.manga_url
        soup = Downloader.requesting_soup(url)
        # print(url)
        # exit()
        
        # print(soup.prettify())
        
        main_container = soup.find('div', {'id': 'chapters'}).find('div')
        for index, a in enumerate(main_container.find_all('a')[::-1]):
            chapter_url = self.main_url + a['href']
            # print(chapter_url)
            
            chapter_soup = Downloader.requesting_soup(chapter_url)
            # print(chapter_soup.prettify())
            # exit()
            
            images = chapter_soup.find_all('img')
            index_val = 0
            
            for image in images:
                # print(image)
                image_src = image["data-src"]
                print(image_src)
                
                # url_re.urlretrieve(image_src, str(index_val))
                # number += 1


if __name__ == '__main__':
    
    download_loc = "C:\\Downloaded_manga"
    # which_manga = input('Enter Manga:')
    which_manga = 'tokidoki'
    
    options = Downloader.manga_options(which_manga)
    
    # print('-----------------------------------------------------')
    # df = pd.DataFrame(options.keys(), columns=['Manga'])
    # df.index += 1
    # print(df)
    # print('-----------------------------------------------------')
    
    # which_one = int(input('Which one(Please enter index number):'))-1
    which_one = 0
    dicts_keys = list(options.keys())
    
    
    obj = Downloader(dicts_keys[which_one], options[dicts_keys[which_one]], download_loc)
    obj.download()