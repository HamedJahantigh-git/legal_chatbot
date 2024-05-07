from bs4 import BeautifulSoup
import requests
import pandas as pd

import warnings
from tqdm import tqdm 

from abc import ABC, abstractmethod

class Crawler(ABC):
    
    @abstractmethod
    def crawl_test(url: str) -> str:
        pass

class VoteCrawler(Crawler):
    
    def __init__(self, base_url: str, result_path: str, vote_spliter = "@") -> None:
        super().__init__()
        self._base_url = base_url
        self._result_path = result_path
        self._vote_spliter = vote_spliter
       
    def crawl_test(url: str) -> str:
        pass 
    
    def check_valid_vote(self, html_soup: BeautifulSoup) -> bool:
        #Extract title for detection of non valid vote
        h1_element = html_soup.find('h1', class_='Title3D')
        span_text = h1_element.find('span').text  # Text within the <span> tag
        full_text = h1_element.text  # Full text within the <h1> element
        text_after_span = full_text.split(span_text)[-1].strip()  # Extract text after the </span> tag
        return len(text_after_span) > 0
    
    def html_data_extracter(self, html_soup: BeautifulSoup) -> str:
        vote_text = html_soup.find('div', id='treeText', class_='BackText')
        title = html_soup.find('h1', class_='Title3D')
        info = html_soup.find('td', valign="top", class_="font-size-small")
        #for sepreting each vote in file use vote_splitter
        vote_df = str(title) + str(info) + str(vote_text) + self._vote_splitter
        return vote_df
    
    def crawl(self, start: int, end: int):
        counter = 0; # for counting right votes crawled
        result_list = []
        warnings.filterwarnings("ignore")
        #loop for send request for get each vote page
        for i in tqdm(range(start, end)):
            #save every 1000 records gotten in .txt format
            if (counter%1000 == 0 and counter > 0) or i == end-1:
                text_file = open(self._result_path + f'vote{i}.txt', "w", encoding='utf-8')
                text_file.write(''.join(result_list))
                text_file.close()
                result_list = []
            url = self._base_url + f"{i}"
            response = requests.get(url, verify=False)
            #change format for persian text
            response.encoding = 'utf-8'
            resp_text = response.text
            html_soup = BeautifulSoup(resp_text, 'html.parser')
            if response.ok and self.check_valid_vote(html_soup):
                counter += 1
                vote_df = self.html_data_extracter(html_soup)
                result_list.append(vote_df)


# class LawNameCrawler(Crawler):
    
    

class TelegramCrawler():
    
    def __init__(self) -> None:
        pass
    
    def channel_html_to_df(self, path:str) -> pd.DataFrame:
        with open(path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        divs_with_text_class = soup.find_all('div', class_='text')
        for div in divs_with_text_class:
            text_content = div.get_text(separator='\n')
            print(text_content)