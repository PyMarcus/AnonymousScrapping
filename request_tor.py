import multiprocessing
import time
from typing import Any
# pip install pysocks
import configparser as configparser
from requests import Session, get
from bs4 import BeautifulSoup
import re



class AnonymousScrapping:
    """Make a scrapping in a site
    :param site: str
    :param tag_link : str
    :param tag_title: str
    :param tag_paragraph
    """
    def __init__(self, site: str, tag_link: str, tag_title: str, tag_paragraph: str) -> None:
        self.__site = site.replace('"', '')
        self.__tag_link = tag_link.replace('"', '')
        self.__tag_title = tag_title.replace('"', '')
        self.__tag_paragraph = tag_paragraph.replace('"', '')

    # get methods
    @property
    def site(self) -> str:
        return self.__site

    @property
    def tag_link(self) -> str:
        return self.__tag_link

    @property
    def tag_title(self) -> str:
        return self.__tag_title

    @property
    def tag_paragraph(self) -> str:
        return self.__tag_paragraph

    @site.setter
    def site(self, new_url) -> None:
        self.__site = new_url

    @tag_link.setter
    def tag_link(self, new_tag_link) -> None:
        self.__tag_link = new_tag_link

    @tag_title.setter
    def tag_title(self, new_tag_title) -> None:
        self.__tag_title = new_tag_title

    # @override
    def __str__(self, any: Any) -> str:
        return f"-> {any}"

    def request(self):
        """Make a request to site"""
        session = Session()
        session.proxies = AnonymousScrapping.proxy()
        return session.get(self.__site.replace('"', ''))

    def htmlParse(self):
        """Parse html with bs4"""
        response = self.request()
        #print(f"[*] {response}")
        if response.status_code == 200:
            bs = BeautifulSoup(response.content, 'html.parser')
            title = bs.find(self.__tag_title).text
            internals_links = bs.find_all(self.__tag_link)
            links = [link['href'] for link in internals_links if 'href' in link.attrs]
            new = []
            for link in links:
                if AnonymousScrapping.regex_links(str(link), title) != []:
                    new.append(AnonymousScrapping.regex_links(str(link), title))
            paragrap = bs.find_all(self.__tag_paragraph)
            text = []
            for p in paragrap:
                text.append(p.text.strip())
            return title, new, text
        else:
            print(f"[*]Fail {response.status_code}")

    def print(self):
        title = self.htmlParse()[0]
        links = [x for x in self.htmlParse()[1]]
        paragraphs = self.htmlParse()[2]
        print(f"[*] status code 200")
        print()
        print(f"[*] TITLE: {title}")
        print()
        print(f"[*] Internals Paths {links}")
        print()
        print(f"[*] CONTENT: {paragraphs}")

    @staticmethod
    def proxy(port: int = 9050, socks: str = "socks5", protocol: str = "http") -> dict:
        """Create config for proxy"""
        proxy: dict = {
            f"{protocol}": f"{socks}://127.0.0.1:{port}"
        }
        return proxy

    @staticmethod
    def regex_links(palavra, keyword):
        """filter keywords"""
        regex = re.compile(f"^(/wiki/{keyword.lower().strip()}?\w+)")
        item = regex.findall(palavra.lower().strip().replace("'", ''))
        return item



if __name__ == '__main__':
    import FoxDot
    FoxDot.pluck()
    time.sleep(2)

    pageItems = configparser.ConfigParser()
    pageItems.read("file.ini")
    tags = [(key, value) for (key, value) in pageItems['tags'].items()]
    anony = AnonymousScrapping(tags[0][1], tags[2][1], tags[1][1], tags[3][1])
    mp = multiprocessing.Process(target=anony.print, args=())
    mp.start()
    mp.join()
    FoxDot.pluck().stop()