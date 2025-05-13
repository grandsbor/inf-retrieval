import os
import pytest

from index import Index
from indexer import Indexer
from searcher import BaseSearcher


TEST_INDEX = 'test_index.inv'


def add_doc(root, name: str, content: str):
    with open(root / f"{name}.txt", "w") as fw1:
        fw1.write(content)


@pytest.fixture(scope="session")
def collection1(tmp_path_factory):
    root = tmp_path_factory.mktemp("collection1")
    add_doc(root, "doc1",
            "Первый документ в коллекции. Важный документ.")
    return root


@pytest.fixture(scope="session")
def collection2(tmp_path_factory):
    root = tmp_path_factory.mktemp("collection2")
    add_doc(root, "doc1",
            "С высокой яблони на Ньютона упало яблоко.")
    add_doc(root, "doc2",
            "Для яблок характерно высокое содержание пищевых волокон.")
    add_doc(root, "doc3",
            "Яблоки были зеленые и твердые.")
    return root


@pytest.mark.hw1
def test_empty_index():
    i = Index()
    i.save(TEST_INDEX)
    assert os.path.isfile(TEST_INDEX)

    i2 = Index()
    i2.load(TEST_INDEX)
    assert i2.get('слово') == []


@pytest.mark.hw1
def test_doc_no():
    i = Index()
    assert i.add_doc("doc0") == 0
    assert i.add_doc("doc1") == 1
    i.save(TEST_INDEX)
    
    i2 = Index()
    i2.load(TEST_INDEX)
    assert i2.add_doc("doc2") == 2


@pytest.mark.hw1
def test_index_base(collection1):
    idxr = Indexer(collection1, TEST_INDEX)
    assert os.path.isfile(TEST_INDEX)
    i = Index()
    i.load(TEST_INDEX)
    assert len(i.docs) == 1
    assert len(i.index) == 5


@pytest.mark.hw1
def test_search_single_term(collection1):
    idxr = Indexer(collection1, TEST_INDEX)
    s = BaseSearcher(TEST_INDEX)
    assert s.search("слово") == []
    assert s.search("документ") == [0]
    # test normalization
    assert s.search("Документ") == [0]
    assert s.search("коллекция") == [0]


@pytest.mark.hw1
def test_search_bool_and(collection2):
    idxr = Indexer(collection2, TEST_INDEX)
    s = BaseSearcher(TEST_INDEX)
    assert sorted(s.search("яблоко")) == [0, 1, 2]
    assert sorted(s.search("высокий AND высокий")) == [0, 1]
    assert sorted(s.search("высокий AND яблоко")) == [0, 1]
    assert s.search("высокий AND упасть") == [0]
    assert s.search("высокий AND ньютон AND на") == [0]
    assert s.search("высокий AND низкий") == []
    with pytest.raises(AssertionError):
        s.search("высокий яблоня")


@pytest.mark.hw1
@pytest.mark.skip
def test_search_bool_or(collection2):
    idxr = Indexer(collection2, TEST_INDEX)
    s = BaseSearcher(TEST_INDEX)
    assert sorted(s.search("высокий OR высокий")) == [0, 1]
    assert sorted(s.search("высокий OR зелёный")) == [0, 1, 2]
    assert sorted(s.search("твёрдый OR зелёный")) == [2]
    assert sorted(s.search("синий OR зелёный")) == [2]


@pytest.mark.hw1
@pytest.mark.skip
def test_multiple_parses(collection2):
    idxr = Indexer(collection2, TEST_INDEX)
    s = BaseSearcher(TEST_INDEX)
    assert sorted(s.search("яблоко AND быть")) == [2]
    assert sorted(s.search("яблоко AND быль")) == [2]


@pytest.mark.hw1
@pytest.mark.skip
def test_return_doc_names(collection2):
    idxr = Indexer(collection2, TEST_INDEX)
    s = BaseSearcher(TEST_INDEX)
    assert sorted(s.search("яблоко", use_doc_names=True)) \
        == ["doc1.txt", "doc2.txt", "doc3.txt"]
    assert sorted(s.search("высокий AND яблоко", use_doc_names=True)) \
        == ["doc1.txt", "doc2.txt"]


@pytest.mark.hw1
@pytest.mark.skip
def test_stopwords(collection2):
    stopwords = ['для', 'и', 'на', 'с']
    idxr = Indexer(collection2, TEST_INDEX, stopwords=stopwords)

    i = Index()
    i.load(TEST_INDEX)
    assert i.get('и') == []

    s = BaseSearcher(TEST_INDEX, stopwords=stopwords)
    assert sorted(s.search("для AND яблоко")) == [0, 1, 2]
    assert sorted(s.search("высокий AND яблоко")) == [0, 1]
    assert s.search("и") == []
    assert s.search("яблоко") == [0, 1, 2]


@pytest.mark.hw1
@pytest.mark.skip
def test_stopwords_normalization(collection2):
    idxr = Indexer(collection2, TEST_INDEX, stopwords=['быть'])
    s = BaseSearcher(TEST_INDEX, stopwords=['быть'])
    assert sorted(s.search("быть AND яблоко")) == [0, 1, 2]
    assert s.search("быль AND яблоко") == [2]
