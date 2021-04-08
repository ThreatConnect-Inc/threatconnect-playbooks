#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from json import loads, dumps
from collections import Counter, defaultdict
from itertools import chain

from .spamsum import spamsum

BLOCK_SIZE = 100
NGRAM_LEN = 5

registry = defaultdict(set)  # ngram -> {source...}


def get_digest(path):
    s = open(path).read()
    digest_len = len(s) / BLOCK_SIZE
    return spamsum(s, block_size=BLOCK_SIZE, digest_len=digest_len)


def _ngrams(s):
    for i in range(len(s) - NGRAM_LEN + 1):
        yield s[i : i + NGRAM_LEN]


def update_registry(digest, source):
    for ngram in _ngrams(digest):
        registry[ngram].add(source)


def find_best_match(digest):
    sources = chain.from_iterable(registry[ngram] for ngram in _ngrams(digest))
    counter = Counter(sources)

    if not counter:
        return None, 0

    (most_common_source,) = counter.most_common(1)
    source, frequency = most_common_source
    return source, frequency


def load_registry():
    registry.clear()

    try:
        saved = loads(open('registry.dat').read())

        for ngram, sources in saved:
            registry[ngram] = set(sources)
    except IOError:
        pass


def dump_registry():
    data = [(ngram, list(sources)) for ngram, sources in registry.items()]
    open('registry.dat', 'w').write(dumps(data))


def main():
    if len(argv) != 3:
        print('Usage: ./ngram.py subcommand path')
        print('Subcommands: u, update, s, search')
        return

    command, path = argv[1:]
    digest = get_digest(path)

    if len(digest) < NGRAM_LEN:
        message = 'error: got digest "%s" shorter than %d bytes'
        print(message % (digest, NGRAM_LEN))
        return

    if command in ['u', 'update']:
        load_registry()
        update_registry(digest, path)
        dump_registry()
    elif command in ['s', 'search']:
        load_registry()
        print(find_best_match(digest))
    else:
        print('error: unknown command', command)


if __name__ == '__main__':
    main()
