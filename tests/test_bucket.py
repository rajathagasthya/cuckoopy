import pytest

from cuckoopy.bucket import Bucket


@pytest.fixture
def bucket():
    return Bucket()


def test_insert(bucket):
    assert bucket.insert('fake_value')


def test_insert_bucket_full(bucket):
    for i in range(bucket.size):
        bucket.insert('fake_value1')
    assert not bucket.insert('fake_value2')


def test_bucket_full(bucket):
    for i in range(bucket.size):
        bucket.insert('fake_value')
    assert bucket.is_full()


def test_bucket_delete(bucket):
    fake_delete_value = 'fake_delete_value'
    bucket.insert(fake_delete_value)
    assert bucket.delete(fake_delete_value)
    assert fake_delete_value not in bucket


def test_bucket_delete_non_existent_value(bucket):
    assert not bucket.delete('fake_non_existent_value')


def test_bucket_contains(bucket):
    bucket.insert('fake_value')
    assert 'fake_value' in bucket


def test_swap(bucket):
    fake_value = 'fake_value'
    fake_swap_value = 'fake_swap_value'
    bucket.insert(fake_value)
    swapped_item = bucket.swap(fake_swap_value)
    assert fake_swap_value in bucket
    assert swapped_item == fake_value
