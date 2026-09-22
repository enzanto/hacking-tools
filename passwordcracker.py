import hashlib
from tqdm import tqdm

from filehandler import read_list


class PasswordCracker:
    def __init__(self):
        self.cracked: list = []
        self.wordlist: str | None = None
        self.hash_type: str | None = None

    def verify_hash(self):
        teststring = "test"
        return teststring

    def hash_cracker(self, hash: str, wordlist: str, hash_type: str = "md5"):
        """Function to compare hashes to wordlists

        Takes a string of hashed values and compares it to the hashed value of words
        in a wordlist. It can use different hashing methods.

        args:
            hash (str): A string with the target hash
            wordlist (str): A string with the path to the wordlist file
            hash_type (str): A string representing the hashing method to use.

        returns:
            str | None: A string if password is cracked, else None is returned."""
        hash_names = [
            "blake2b",
            "blake2s",
            "md5",
            "sha1",
            "sha224",
            "sha256",
            "sha384",
            "sha3_224",
            "sha3_256",
            "sha3_384",
            "sha3_512",
            "sha512",
        ]
        words = read_list(wordlist, mode="rb")
        total_lines = sum(1 for _ in words)
        hash_func = getattr(hashlib, hash_type, None)
        if hash_func is None or hash_type not in hash_names:
            raise ValueError()
        loot = None
        for line in tqdm(words, desc="Cracking hash", total=total_lines):
            try:  # skips entries that are not utf-8 encoded
                decoded_line = line.decode().strip()
                if hash_func(decoded_line.encode()).hexdigest() == hash:
                    self.cracked.append((hash, decoded_line))
                    loot = decoded_line
                    break
            except UnicodeDecodeError:
                continue
        if loot is not None:
            print(f"Added to loot: {loot}")
        return loot


if __name__ == "__main__":
    wordlist = (
        "/home/fredrik/Documents/Noroff/fag/EP2/hacking-tools/wordlist/rockyou.txt"
    )
    # hash = "e99a18c428cb38d5f260853678922e03"
    # hash = "07d10604216a46ce7439b32cfa7bcdd6"
    pwd = "!!Boom!!"
    # pwd = "password123"
    hash = hashlib.md5(pwd.encode()).hexdigest()
    test = PasswordCracker()
    test.hash_cracker(hash=hash, wordlist=wordlist)
