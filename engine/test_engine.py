import os
import pytest

from index import Index
from indexer import Indexer


TEST_INDEX = 'test_index.inv'


@pytest.fixture(scope="session")
def collection(tmp_path_factory):
    root = tmp_path_factory.mktemp("collection")
    with open(root / "doc1.txt", "w") as fw1:
        fw1.write("Первый документ в коллекции")
    return root

def test_empty_index():
    i = Index()
    i.save(TEST_INDEX)
    assert os.path.isfile(TEST_INDEX)

    i2 = Index()
    i2.load(TEST_INDEX)
    assert i2.get('слово') == []
    os.remove(TEST_INDEX)

def test_doc_no():
    i = Index()
    assert i.add_doc("doc0") == 0
    assert i.add_doc("doc1") == 1
    i.save(TEST_INDEX)
    
    i2 = Index()
    i2.load(TEST_INDEX)
    assert i2.add_doc("doc2") == 2

def test_indexer(collection):
    idxr = Indexer(collection, TEST_INDEX)
    assert os.path.isfile(TEST_INDEX)
    i = Index()
    i.load(TEST_INDEX)
    assert len(i.docs) == 1
    assert len(i.index) == 4
    os.remove(TEST_INDEX)