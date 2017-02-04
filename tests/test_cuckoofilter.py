import pytest

from cuckoopy.cuckoofilter import CuckooFilter
from cuckoopy.exceptions import CuckooFilterFullException


@pytest.fixture
def cuckoo_filter():
    return CuckooFilter(capacity=100, fingerprint_size=1)


def test_insert(cuckoo_filter):
    assert cuckoo_filter.insert('fake_insert_value')


def test_insert_alternate_location(cuckoo_filter):
    pass


def test_insert_filter_full(cuckoo_filter):
    pass


def test_delete(cuckoo_filter):
    fake_delete_value = 'fake_delete_value'
    cuckoo_filter.insert(fake_delete_value)
    assert cuckoo_filter.delete(fake_delete_value)
    assert not cuckoo_filter.contains(fake_delete_value)


def test_delete_non_existent_value(cuckoo_filter):
    assert not cuckoo_filter.delete('fake_non_existent_value')


def test_size(cuckoo_filter):
    insert_values = ['fake_value1', 'fake_value2']
    for val in insert_values:
        cuckoo_filter.insert(val)
    assert cuckoo_filter.size == len(insert_values)
