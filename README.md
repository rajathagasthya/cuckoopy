# cuckoopy: Pure Python (python3) implementation of Cuckoo Filter data structure

Cuckoo Filter, like Bloom Filter, is a probabilistic data structure for fast,
approximate set membership queries, with some small false positive probability.
While Bloom Filters are space efficient and are widely used, they do not
support deletion of items from the set without rebuilding the entire filter.
This can be overcome with several extensions to Bloom Filters such as
Counting Bloom Filters, but with significant space overhead.

Cuckoo Filters support adding and removing items dynamically while achieving
higher performance than Bloom filters. A Cuckoo Filter is based on partial-key
cuckoo hashing that stores only fingerprint of each item inserted. Cuckoo
Filters provide higher lookup performance than Bloom Filters and uses less
space than Bloom Filters if the target false positive rate is < 3%.

The original research paper ["Cuckoo Filter: Better Than Bloom" by Bin Fan,
Dave Andersen and Michael Kaminsky](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)
describes the data structure in more detail.

## Usage
```python
>>> from cuckoopy import CuckooFilter
# Initialize a cuckoo filter with 10000 buckets with bucket size 4 and fingerprint size of 1 byte
>>> cf = CuckooFilter(capacity=10000, bucket_size=4, fingerprint_size=1)
```
Insert an item into the filter:
```python
>>> cf.insert('Hello!')
True
```
Lookup an item in the filter:
```python
>>> cf.contains('Hello!')
True
>>> 'Hello!' in cf
True
```
Delete an item from the filter:
```python
>>> cf.delete('Hello!')
True
```
Get the size (number of items present) of the filter:
```python
>>> cf.size
4
>>> len(cf)
4
```

## Running tests locally
This project uses [pytest](http://docs.pytest.org) for tests. Make sure you
have `tox` installed on your local machine and from the root directory of the
project, run:

```
$ tox
```
This command runs unit tests in python 3.5 and python 3.6 environments with
code coverage details. It also runs pep8 (flake8) checks. To run tox against a
specific environment (py35, py36 or pep8), use the `-e` option.


## License
[MIT License] (/LICENSE)


## Useful Links
- [Probabilistic Filters By Example](https://bdupras.github.io/filter-tutorial/)
- [Original C++ implementation by the authors of the research paper](https://github.com/efficient/cuckoofilter)
