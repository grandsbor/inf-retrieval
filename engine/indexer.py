import os
import os.path
from index import Index


class Indexer:
    def __init__(self, path: str, index_file='index.inv'):
        index = Index()
        for fname in os.listdir(path):
            if not fname.endswith('.txt'):
                continue
            fullpath = os.path.join(path, fname)
            doc_no = index.add_doc(fullpath)
            with open(fullpath, encoding='utf8') as fh:
                for line in fh:
                    tokens = line.strip().lower().split()
                    for token in tokens:
                        if not token.isalpha():
                            continue
                        index.add(doc_no, token)
        index.save(index_file)


if __name__ == "__main__":
    path = "YOUR PATH HERE"
    i = Indexer(path)