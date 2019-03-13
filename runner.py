from collections import Counter
import re
import timeit
from src.VPTree import VPTree


def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('data/big.txt').read()))

start_build = timeit.default_timer()
tree = VPTree(list(WORDS.keys()), WORDS)
print('build_time', timeit.default_timer() - start_build)

n_neighbors = [5, 10, 15, 20, 25, 30]
for n in n_neighbors:
    print(tree.knn('speeelling', n))

print(tree.knn('bannana', 5))
print(tree.knn('banna', 5))
print(tree.knn('bana', 5))
print(tree.knn('baa', 5))
print(tree.knn('ba', 5))

