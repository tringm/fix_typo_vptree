import string
import re
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())


def P(word, N=sum(WORDS.values())):
    print("Probability of word:" + word, WORDS[word] / N)
    return WORDS[word] / N


def correction(word):
    "Most probable spelling correction for word."

    if word in WORDS:
        return word

    word_candidates = candidates(word)
    # print('Candidates', word_candidates)
    return max(candidates(word), key=P)


def candidates(word, max_depth=10):
    candidates_in_dictionary = None
    for depth in range(max_depth):
        if depth == 0:
            edited_words = edits(word)
        else:
            new_edited_words = set()
            for edited_w in edited_words:
                new_edited_words = new_edited_words.union(edits(edited_w))
            edited_words = new_edited_words
        candidates_in_dictionary = known(edited_words)
        if candidates_in_dictionary:
            break
    if not candidates_in_dictionary:
        candidates_in_dictionary = [word]
    return candidates_in_dictionary


def known(words):
    return set(w for w in words if w in WORDS)


def edits(word):
    """
    All possible edits of word
    Operations:
        Deleted
        Transposed
        Replaced
        Inserted
    :param word:
    :return:
    """
    letters = string.ascii_lowercase
    splitted_pairs = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deleted = [left + right[1:] for left, right in splitted_pairs if right]
    transposed = [left + right[1] + right[0] + right[2:] for left, right in splitted_pairs if len(right) > 1]
    replaced = [left + c + right[1:] for left, right in splitted_pairs if right for c in letters]
    inserted = [left + c + right for left, right in splitted_pairs for c in letters]
    return set(deleted + transposed + replaced + inserted)


print(correction('speeeeeling'))
