import json
from collections import defaultdict
from pymorphy3 import MorphAnalyzer


class Index:
    def __init__(self):
        self.index = defaultdict(list)
        self.docs = []
        self.morph = MorphAnalyzer()

    def _normalize(self, raw_term: str) -> str | None:
        parse = self.morph.parse(raw_term)
        if parse:
            return parse[0].normal_form

    def add_doc(self, doc_name: str) -> int:
        self.docs.append(doc_name)
        return len(self.docs) - 1

    def add(self, doc_no: int, raw_term: str) -> None:
        term = self._normalize(raw_term)
        if term:
            if term not in self.index or self.index[term][-1] != doc_no:
                self.index[term].append(doc_no)

    def get(self, term: str) -> list[int]:
        return self.index.get(term, [])

    def save(self, fname: str):
        with open(fname, 'w') as fh:
            json.dump({
                'index': self.index,
                'docs': self.docs,
            }, fh)

    def load(self, fname: str):
        with open(fname) as fh:
            temp = json.load(fh)
            self.index, self.docs = temp['index'], temp['docs']


class PositionalIndex(Index):
    def __init__(self):
        super().__init__()
        self.index = defaultdict(dict)
        self.title_index = defaultdict(dict)

    def add(self, doc_no: int, raw_term: str, pos: int, is_title: bool) -> None:
        term = self._normalize(raw_term)
        if term:
            index = self.title_index if is_title else self.index
            if doc_no not in index[term]:
                index[term][doc_no] = []
            index[term][doc_no].append(pos)

    def get(self, term: str) -> dict[int, list[int]]:
        return self.index.get(term, {})

    def load(self, fname: str):
        with open(fname) as fh:
            temp = json.load(fh)
            self.docs = temp['docs']
            for term, posting in temp['index'].items():
                for doc_no, positions in posting.items():
                    self.index[term][int(doc_no)] = positions
