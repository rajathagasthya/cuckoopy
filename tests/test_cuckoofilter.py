import os
import pytest

import cuckoopy.hashutils as hashutils

from cuckoopy.cuckoofilter import CuckooFilter
from cuckoopy.exceptions import CuckooFilterFullException


@pytest.fixture
def cuckoo_filter():
    return CuckooFilter(capacity=100, fingerprint_size=1)


@pytest.fixture
def cf():
    return CuckooFilter(capacity=400000, fingerprint_size=1)


def test_insert(cuckoo_filter):
    assert cuckoo_filter.insert('fake_insert_value')


def test_insert_alternate_location(cuckoo_filter):
    fake_value = 'fake_value'
    # When bucket_size + 1 values are inserted, the one bucket will be full
    # and the other bucket will have a size of 1.
    for _ in range(cuckoo_filter.bucket_size + 1):
        cuckoo_filter.insert(fake_value)
    first_index = cuckoo_filter._get_index(fake_value)
    fingerprint = hashutils.fingerprint(fake_value,
                                        cuckoo_filter.fingerprint_size)
    alt_index = cuckoo_filter._get_alternate_index(first_index, fingerprint)
    first_bucket = cuckoo_filter.buckets[first_index]
    alt_bucket = cuckoo_filter.buckets[alt_index]
    assert len(first_bucket) == cuckoo_filter.bucket_size
    assert len(alt_bucket) == 1


def test_insert_filter_full(cuckoo_filter):
    # We can artificially make a filter full by inserting the same item
    # (2 * bucket size) times, so another insert of the same item should fail.
    fake_value = 'fake_value'
    for _ in range(2 * cuckoo_filter.bucket_size):
        cuckoo_filter.insert(fake_value)
    with pytest.raises(CuckooFilterFullException):
        cuckoo_filter.insert(fake_value)


@pytest.mark.skipif(not os.path.isfile('/usr/share/dict/words'),
                    reason='Dictionary file /usr/share/dict/words'
                           'does not exist')
def test_insert_large_number_of_values(cf):
    with open('/usr/share/dict/words') as f:
        words = f.readlines()
    for word in words:
        cf.insert(word.strip())
    assert len(cf) == len(words)


def test_delete(cuckoo_filter):
    fake_delete_value = 'fake_delete_value'
    cuckoo_filter.insert(fake_delete_value)
    assert cuckoo_filter.delete(fake_delete_value)
    assert not cuckoo_filter.contains(fake_delete_value)


def test_delete_non_existent_value(cuckoo_filter):
    assert not cuckoo_filter.delete('fake_non_existent_value')


@pytest.mark.skipif(not os.path.isfile('/usr/share/dict/words'),
                    reason='Dictionary file /usr/share/dict/words'
                           'does not exist')
def test_delete_large_number_of_values(cf):
    with open('/usr/share/dict/words') as f:
        words = f.readlines()
    words = [w.strip() for w in words]
    for word in words:
        cf.insert(word)
    assert len(cf) == len(words)
    deleted = True
    for word in words:
        if not cf.delete(word):
            deleted = False
    assert deleted


def test_size(cuckoo_filter):
    insert_values = ['fake_value1', 'fake_value2']
    for val in insert_values:
        cuckoo_filter.insert(val)
    assert cuckoo_filter.size == len(insert_values)
    assert len(cuckoo_filter) == len(insert_values)


def test_contains(cuckoo_filter):
    fake_value = 'fake_value'
    cuckoo_filter.insert(fake_value)
    assert cuckoo_filter.contains(fake_value)
    assert fake_value in cuckoo_filter


@pytest.mark.skipif(not os.path.isfile('/usr/share/dict/words'),
                    reason='Dictionary file /usr/share/dict/words'
                           'does not exist')
def test_contains_large_number_of_values(cf):
    with open('/usr/share/dict/words') as f:
        words = f.readlines()
    words = [w.strip() for w in words]
    for word in words:
        cf.insert(word)
    assert len(cf) == len(words)
    contains = True
    for word in words:
        if not cf.contains(word):
            contains = False
    assert contains


def test_contains_non_existent_value(cuckoo_filter):
    fake_value = 'fake_value'
    assert not cuckoo_filter.contains(fake_value)
    assert fake_value not in cuckoo_filter
