import requests
from tqdm import tqdm


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

        words = self._get_words(wordlist)
        headers = {"User-Agent": self.agent}
        for i in tqdm(words, desc="Brute forcing directories", total=len(words)):
            if "." in i:
                url = f"{self.target}/{i}"
            else:
                url = f"{self.target}/{i}/"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                self.loot.append(url)


if __name__ == "__main__":
    t = DirectoryBuster()
    t.directory_brute(target="10.1.1.39", wordlist="wordlist/common.txt")
    for loot in t.loot:
        print(loot)


### Readlines kept the \n and the end, and split used it to split the words
