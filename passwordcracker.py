import hashlib
from tqdm import tqdm


class PasswordCracker:
    def __init__(self):
        self.cracked: list = []
        self.wordlist: str | None = None
        self.hash_type: str | None = None

    def verify_hash(self):
        teststring = "test"
        return teststring

    def hash_cracker(
        self, hash: str, wordlist: str | None = None, hash_type: str = "md5"
    ):
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

        wordlist = (
            "/home/fredrik/Documents/Noroff/fag/EP2/hacking-tools/wordlist/rockyou.txt"
        )
        total_lines = sum(1 for line in open(wordlist, "rb"))
        hash_func = getattr(hashlib, hash_type, None)
        if hash_func is None or hash_type not in hash_names:
            raise ValueError()
        loot = None
        with open(wordlist, "rb") as f:
            for line in tqdm(f, desc="Cracking hash", total=total_lines):
                try:  # skips entries that are not utf-8 encoded
                    decoded_line = line.decode()
                    if hash_func(decoded_line.strip().encode()).hexdigest() == hash:
                        self.cracked.append(decoded_line)
                        loot = decoded_line
                        break
                except UnicodeDecodeError:
                    continue
        if loot is not None:
            print(f"Added to loot: {loot}")


if __name__ == "__main__":
    # hash = "e99a18c428cb38d5f260853678922e03"
    # hash = "07d10604216a46ce7439b32cfa7bcdd6"
    pwd = "0125457423"
    # pwd = "password123"
    hash = hashlib.md5(pwd.encode()).hexdigest()
    test = PasswordCracker()
    test.hash_cracker(hash=hash)
