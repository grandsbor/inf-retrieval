import os
import os.path
import string

from index import Index, PositionalIndex


class Indexer:
    def __init__(self, path: str, index_path='index.inv', stopwords=None):
        index = self._init_index()
        for fname in sorted(os.listdir(path)):
            if not fname.endswith('.txt'):
                continue
            fullpath = os.path.join(path, fname)
            doc_no = index.add_doc(fullpath)
            self._process_one_doc(index, fullpath, doc_no)
        index.save(index_path)

    def _init_index(self):
        return Index()

    def _tokenize_one_line(self, line: str) -> list[str]:
        tokens = line.strip().lower().split()
        return [
            ''.join(c for c in token if c not in string.punctuation)
            for token in tokens if token
        ]

    def _process_one_doc(self, index, fullpath, doc_no):
        with open(fullpath, encoding='utf8') as fh:
            for line in fh:
                for token in self._tokenize_one_line(line):
                    index.add(doc_no, token)


class PositionalIndexer(Indexer):
    def _init_index(self):
        return PositionalIndex()

    def _process_one_doc(self, index, fullpath, doc_no):
        with open(fullpath, encoding='utf8') as fh:
            pos = 0
            for line in fh:
                for token in self._tokenize_one_line(line):
                    index.add(doc_no, token, pos, False)
                    pos += 1


if __name__ == "__main__":
    path = "YOUR PATH HERE"
    i = Indexer(path)