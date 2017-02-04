import random


class Bucket(object):

    def __init__(self, size=4):
        self.size = size
        self.bucket = []

    def __repr__(self):
        return '<Bucket: ' + str(self.bucket) + '>'

    def __contains__(self, item):
        return item in self.bucket

    def __len__(self):
        return len(self.bucket)

    def insert(self, item):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        if not self.is_full():
            self.bucket.append(item)
            return True
        return False

    def delete(self, item):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        try:
            del self.bucket[self.bucket.index(item)]
            return True
        except ValueError:
            return False

    def is_full(self):
        return len(self.bucket) == self.size

    def swap(self, item):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param item:
        :return:
        """
        index = random.choice(range(len(self.bucket)))
        swapped_item = self.bucket[index]
        self.bucket[index] = item
        return swapped_item
