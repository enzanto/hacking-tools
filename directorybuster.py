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
        self.loot = {}
        self.words = []

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
        loot = {}
        loot[target] = []
        self.loot[target] = []
        headers = {"User-Agent": self.agent}
        s = requests.Session()
        try:
            for i in tqdm(words, desc="Brute forcing directories", total=len(words)):
                if "." in i:
                    url = f"{target}/{i}"
                else:
                    url = f"{target}/{i}/"
                r = s.get(url, headers=headers)
                if r.status_code == 200:
                    self.loot[target].append(url)
        except TypeError as e:
            print(e)
        return loot

    def subdomain_brute(self, target: str, wordlist: str):
        """A function to brute force subdomains from a wordlist

        This function takes the wordlist, and sends in to _get_words to retrieve a list
        then it filters out invalid subdomain types by regex, before testing the subdomain
        prefixes are removed. Subdomains woth a valid 200 response is added to loot.

        args:
            target (str): The base URL of the targets
            wordlist (str): The location of the wordlist file

        returns:
            loot (list[str]): Returns a list of strings with successful directories or files"""
        pattern = "^[a-zA-Z0-9]+[a-zA-Z0-9-][a-zA-Z0-9]+$"
        word_list = []
        # Removes the prefix in two steps, to ensure http:// and www is not present
        sanitized_target = target.removeprefix("http://").removeprefix("www.")
        self.loot[sanitized_target] = []
        raw_words = read_list(wordlist)
        try:
            for word in raw_words:
                if re.search(pattern, word):
                    word_list.append(word.lower())

            words = set(word_list)
        except TypeError as e:
            print(f"{e}")
            return "File not found"
        headers = {"User-Agent": self.agent}
        for i in tqdm(words, desc="Brute forcing directories", total=len(words)):
            url = f"https://{i}.{sanitized_target}"
            try:
                r = requests.get(url, headers=headers, timeout=5)
                if r.status_code == 200:
                    self.loot[sanitized_target].append(url)
            except requests.exceptions.RequestException:
                continue
            finally:
                time.sleep(0.15)  # sleep timer to avoid rate limit with DNS queries


if __name__ == "__main__":
    t = DirectoryBuster()
    host = input("Type the address of the target: ")
    wordlist = input("Type the path to the wordlist: ")
    print("Select scanner:")
    print("1: Sub directory brute")
    print("2: Sub domain brute")
    running = True
    while running:
        selection = input("type your selection number: ")
        if selection == "1":
            t.directory_brute(target=host, wordlist=wordlist)
            running = False
        elif selection == "2":
            t.subdomain_brute(target=host, wordlist=wordlist)
            running = False
        else:
            print("invalid selection")
    save = input("Do you want to save loot to file? y/n: ")
    if save.lower() == "y":
        import filehandler

        filename = filehandler.write_json(t.loot)
        print(f"Loot saved to {filename}")
