class directoryBuster:
    def __init__(self):
        self.target = None
        self.loot = None
        self.words = []

    def get_words(self):
        wordlist = "wordlist/all.txt"
        extensions = [".php", ".bak", ".orig", ".inc"]
        with open(wordlist) as f:
            words = f.read().split()
        for word in words:
            if "." in word:
                self.words.append(f"/{word}")
            else:
                self.words.append(f"/{word}/")


if __name__ == "__main__":
    t = directoryBuster()
    t.get_words()
    print(t.words[:10])


### Readlines kept the \n and the end, and split used it to split the words
