from index import Index, PositionalIndex


class BaseSearcher:
    def __init__(self, index_path: str, stopwords=None):
        self.index = Index()
        self.index.load(index_path)

    def _search(self, op: str, terms: list[str]) -> list[int]:
        if op == "and":
            return self._search_and(terms)
        return []

    def _search_and(self, terms: list[str]) -> list[int]:
        docs = set(self.index.get(terms[0]))
        for term in terms[1:]:
            docs &= set(self.index.get(term))
        return list(docs)

    def search(self, query: str, use_doc_names: bool = False) -> list[int]:
        tokens = query.lower().split()
        assert len(tokens) % 2 == 1
        op = tokens[1] if len(tokens) > 1 else "and"
        terms = tokens[::2]
        return self._search(op, terms)

class PositionalSearcher(BaseSearcher):
    def __init__(self, index_path: str, stopwords=None):
        self.index = PositionalIndex()
        self.index.load(index_path)

    def _search(self, op: str, terms: list[str]) -> list[int]:
        if op[0] == '/':
            assert len(terms) == 2
            dist = int(op[1:])
            result = []
            docs1 = self.index.get(terms[0])
            docs2 = self.index.get(terms[1])
            for (doc_no, pos1) in docs1.items():
                pos2 = docs2.get(doc_no)
                if pos2:
                    pos2_set: set[int] = set(pos2)
                    for p in pos1:
                        if (p + dist) in pos2_set:
                            result.append(doc_no)
            return result
        return super()._search(op, terms)


if __name__ == "__main__":
    s = BaseSearcher('index.inv')
    query = input("Enter query: ")
    print(s.search(query))