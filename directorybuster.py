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
        words = []
        with open(wordlist) as f:
            raw_words = f.read().split()
        for word in raw_words:
            if "." in word:
                words.append(f"/{word}")
            else:
                words.append(f"/{word}/")
        return words

    def directory_brute(self, target: str, wordlist: str):
        words = self._get_words(wordlist)
        headers = {"User-Agent": self.agent}
        for i in tqdm(words, desc="Brute forcing directories", total=len(words)):
            url = f"{self.target}{i}"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                self.loot.append(url)


if __name__ == "__main__":
    t = DirectoryBuster()
    t.directory_brute(target="10.1.1.39", wordlist="wordlist/common.txt")
    for loot in t.loot:
        print(loot)


### Readlines kept the \n and the end, and split used it to split the words
