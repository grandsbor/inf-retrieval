import json
from pymorphy3 import MorphAnalyzer


class Index:
    def __init__(self):
        self.index = {}
        self.docs = []
        self.morph = MorphAnalyzer()

    def add_doc(self, doc_name: str) -> int:
        self.docs.append(doc_name)
        return len(self.docs) - 1

    def add(self, doc_no: int, raw_term: str) -> None:
        parse = self.morph.parse(raw_term)
        if parse:
            term = parse[0].normal_form
            if term not in self.index:
                self.index[term] = [doc_no]
            elif self.index[term][-1] != doc_no:
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