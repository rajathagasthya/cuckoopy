"""
Cuckoo Filter
"""

import random

from . import bucket
from . import exceptions
from . import hashutils


class CuckooFilter(object):
    """
    Cuckoo Filter class.

    Implements insert, delete and contains operations for the filter.
    """

    def __init__(self, capacity, bucket_size=4, fingerprint_size=1,
                 max_displacements=500):
        """
        Initialize CuckooFilter object.

        :param capacity: Size of the Cuckoo Filter
        :param bucket_size: Number of entries in a bucket
        :param fingerprint_size: Fingerprint size in bytes
        :param max_displacements: Maximum number of evictions before filter is
        considered full
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.max_displacements = max_displacements
        self.buckets = [bucket.Bucket(size=bucket_size)
                        for _ in range(self.capacity)]
        self.size = 0

    def __repr__(self):
        return '<CuckooFilter: capacity=' + str(self.capacity) + \
               ', size=' + str(self.size) + ', fingerprint size=' + \
               str(self.fingerprint_size) + ' byte(s)>'

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return self.contains(item)

    def _get_index(self, item):
        index = hashutils.hash_code(item) % self.capacity
        return index

    def _get_alternate_index(self, index, fingerprint):
        alt_index = (index ^ hashutils.hash_code(fingerprint)) % self.capacity
        return alt_index

    def insert(self, item):
        """
        Insert an item into the filter.

        :param item: Item to be inserted.
        :return: True if insert is successful; CuckooFilterFullException if
        filter is full.
        """
        fingerprint = hashutils.fingerprint(item, self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)

        if self.buckets[i].insert(fingerprint) \
                or self.buckets[j].insert(fingerprint):
            self.size += 1
            return True

        eviction_index = random.choice([i, j])
        for _ in range(self.max_displacements):
            f = self.buckets[eviction_index].swap(fingerprint)
            eviction_index = self._get_alternate_index(eviction_index, f)
            if self.buckets[eviction_index].insert(f):
                self.size += 1
                return True
        # Filter is full
        raise exceptions.CuckooFilterFullException('Insert operation failed. '
                                                   'Filter is full.')

    def contains(self, item):
        """
        Check if the filter contains the item.

        :param item: Item to check its presence in the filter.
        :return: True, if item is in the filter; False, otherwise.
        """
        fingerprint = hashutils.fingerprint(item, self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)

        return fingerprint in self.buckets[i] or fingerprint in self.buckets[j]

    def delete(self, item):
        """
        Delete an item from the filter.

        To delete an item safely, it must have been previously inserted.
        Otherwise, deleting a non-inserted item might unintentionally remove
        a real, different item that happens to share the same fingerprint.

        :param item: Item to delete from the filter.
        :return: True, if item is found and deleted; False, otherwise.
        """
        fingerprint = hashutils.fingerprint(item, size=self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)
        if self.buckets[i].delete(fingerprint) \
                or self.buckets[j].delete(fingerprint):
            self.size -= 1
            return True
        return False
