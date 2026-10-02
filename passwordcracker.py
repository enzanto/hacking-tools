import hashlib
from tqdm import tqdm

from filehandler import read_list


class PasswordCracker:
    def __init__(self):
        self.cracked: dict = {}
        self.wordlist: str | None = None
        self.hash_type: str | None = None

    def verify_hash(self, hash: str):
        hash_lengts = {
            32: ["md5"],
            40: ["sha1"],
            56: ["sha224", "sha3_224"],
            64: ["blake2s", "sha256", "sha3_256"],
            96: ["sha384", "sha3_384"],
            128: ["blake2b", "sha512", "sha3_512"],
        }
        length = len(hash)
        return hash_lengts[length]

    def hash_cracker(
        self,
        wordlist: str,
        hash: str | None = None,
        hashlist: str | None = None,
        hash_type: str | None = None,
    ):
        """Function to compare hashes to wordlists

        Takes a string of hashed values and compares it to the hashed value of words
        in a wordlist. It can use different hashing methods.

        args:
            hash (str): A string with the target hash
            wordlist (str): A string with the path to the wordlist file
            hash_type (str): A string representing the hashing method to use.

        returns:
            str | None: A string if password is cracked, else None is returned."""
        hash_names = {
            "blake2b": hashlib.blake2b,
            "blake2s": hashlib.blake2s,
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha224": hashlib.sha224,
            "sha256": hashlib.sha256,
            "sha384": hashlib.sha384,
            "sha3_224": hashlib.sha3_224,
            "sha3_256": hashlib.sha3_256,
            "sha3_384": hashlib.sha3_384,
            "sha3_512": hashlib.sha3_512,
            "sha512": hashlib.sha512,
        }
        hashes = []
        hash_types = []
        words = read_list(wordlist, mode="rb")
        if hash != None:
            hashes.append(hash)
        if hashlist != None:
            try:
                hsh = read_list(hashlist)
                hashes.extend(hsh)
            except TypeError as e:
                print(f"Could not add hash list: {e}")
        total_lines = sum(1 for _ in words)
        if hash_type != None:
            if hash_type in hash_names:
                hash_types.append(hash_type)
            else:
                raise ValueError()
        else:
            for i in hashes:
                hash_types.extend(self.verify_hash(i))

        loot = {}
        for line in tqdm(words, desc="Cracking hash", total=total_lines):
            try:  # skips entries that are not utf-8 encoded
                decoded_line = line.decode().strip()
                for h in hash_types:
                    hash = hash_names[h](decoded_line.encode()).hexdigest()
                    if hash in hashes:
                        if decoded_line not in self.cracked:
                            self.cracked[decoded_line] = {
                                "password": decoded_line,
                                "hash": hash,
                                "type": h,
                            }
                        loot[decoded_line] = {
                            "password": decoded_line,
                            "hash": hash,
                            "type": h,
                        }
                        break
            except UnicodeDecodeError:
                continue
        for l in loot:
            print(f"Added to loot: {l}")
        return loot


if __name__ == "__main__":
    wordlist = input("Path of wordlist: ")
    hashlist = input("Path of hashlist: ")
    cracker = PasswordCracker()
    cracker.hash_cracker(hashlist=hashlist, wordlist=wordlist)
    save = input("Do you want to save loot to a file? y/n: ")
    if save.lower() == "y":
        import filehandler

        filename = filehandler.write_json(cracker.cracked)
        print(f"Loot saved to {filename}")
