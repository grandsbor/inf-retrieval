from index import Index


class BaseSearcher:
    def __init__(self, index_path: str, stopwords=None):
        self.index = Index()
        self.index.load(index_path)

    def search_and(self, terms: list[str]) -> list[int]:
        docs = set(self.index.get(terms[0]))
        for term in terms[1:]:
            docs &= set(self.index.get(term))
        return list(docs)

    def search(self, query: str, use_doc_names: bool = False) -> list[int]:
        tokens = query.lower().split()
        if len(tokens) == 1:
            return self.index.get(tokens[0])
        assert len(tokens) % 2 == 1
        terms = tokens[::2]
        op = tokens[1]
        if op == "and":
            return self.search_and(terms)


if __name__ == "__main__":
    s = BaseSearcher('index.inv')
    query = input("Enter query: ")
    print(s.search(query))