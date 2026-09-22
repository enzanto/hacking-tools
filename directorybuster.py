import requests
from tqdm import tqdm
import time
import re

from filehandler import read_list


class DirectoryBuster:
    def __init__(self):
        self.target = "http://10.1.1.39"
        self.agent = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:154.0) Gecko/20100101 Firefox/154.0"
        )
        self.loot = []
        self.words = []

    def _get_words(self, wordlist: str):
        """An internal function to provide a list of words

        This functions takes a wordlist provided with one word per line, and splits
        it in to separate words.

        args:
            wordlist (str): A string with the location of the wordlist to open.

        returns (list): A list with words for directory brute"""
        words = []
        with open(wordlist) as f:
            words = f.read().split()
        return words

    def directory_brute(self, target: str, wordlist: str):
        """A function to brute force directory locations from a wordlist

        This function takes the wordlist, and sends in to _get_words to retrieve a list
        and uses that list with the requests module to check for status_code 200 and
        store the found directories to loot variable

        args:
            target (str): The base URL of the targets
            wordlist (str): The location of the wordlist file

        returns:
            loot (list[str]): Returns a list of strings with successful directories or files"""

        words = read_list(wordlist)
        headers = {"User-Agent": self.agent}
        for i in tqdm(words, desc="Brute forcing directories", total=len(words)):
            if "." in i:
                url = f"{self.target}/{i}"
            else:
                url = f"{self.target}/{i}/"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                self.loot.append(url)

    def subdirectory_brute(self, target: str, wordlist: str):
        pattern = "^[a-zA-Z0-9]+[a-zA-Z0-9-][a-zA-Z0-9]+$"
        word_list = []
        raw_words = read_list(wordlist)
        for word in raw_words:
            if re.search(pattern, word):
                word_list.append(word.lower())

        words = set(word_list)
        # words = set(word_list.sort())
        # words = self._get_words(wordlist)
        headers = {"User-Agent": self.agent}
        for i in tqdm(words, desc="Brute forcing directories", total=len(words)):
            url = f"https://{i}.{target}"
            try:
                r = requests.get(url, headers=headers, timeout=5)
                if r.status_code == 200:
                    self.loot.append(url)
            except requests.exceptions.RequestException:
                continue
            finally:
                time.sleep(0.15)  # sleep timer to avoid rate limit with DNS queries


if __name__ == "__main__":
    t = DirectoryBuster()
    t.directory_brute(target="10.1.1.39", wordlist="wordlist/common.txt")
    for loot in t.loot:
        print(loot)


### Readlines kept the \n and the end, and split used it to split the words
