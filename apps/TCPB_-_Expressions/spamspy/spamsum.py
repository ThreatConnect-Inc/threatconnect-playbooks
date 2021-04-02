#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from string import ascii_lowercase, ascii_uppercase, digits

MAX_DIGEST_LEN = 64
MIN_BLOCK_SIZE = 3

MAX_UINT32 = 0xFFFFFFFF


class RollingHash:
    _ROLLING_WINDOW = 7

    def __init__(self):
        self.h1 = 0
        self.h2 = 0
        self.h3 = 0

        self.window = [0] * self._ROLLING_WINDOW
        self.n = 0

    @property
    def hash(self):
        h = self.h1 + self.h2 + self.h3
        return h & MAX_UINT32

    def update(self, c):
        c = ord(c)

        self.h2 -= self.h1
        self.h2 += self._ROLLING_WINDOW * c

        self.h1 += c
        self.h1 -= self.window[self.n % self._ROLLING_WINDOW]

        self.window[self.n % self._ROLLING_WINDOW] = c
        self.n += 1

        self.h3 = (self.h3 << 5) & MAX_UINT32
        self.h3 ^= c


class SumHash:
    def __init__(self):
        self.hash = 0x28021967

    def update(self, c):
        self.hash *= 0x01000193
        self.hash &= MAX_UINT32
        self.hash ^= ord(c)


def _spamsum(s, block_size, digest_len, legacy_mode):
    yielded = 0
    sh = SumHash()
    rh = RollingHash()

    for c in s:
        sh.update(c)
        rh.update(c)

        if (rh.hash % block_size) == (block_size - 1):
            if yielded < (digest_len - 1):
                yield sh.hash
                yielded += 1
                sh = SumHash()

    if rh.hash != 0:
        # No need to yield initial hash, unless mimicing the original
        if legacy_mode or sh.hash != SumHash().hash:
            yield sh.hash


def _block_size(s):
    block_size = MIN_BLOCK_SIZE

    while block_size * MAX_DIGEST_LEN < len(s):
        block_size *= 2

    return block_size


def spamsum(s, block_size=None, digest_len=MAX_DIGEST_LEN, legacy_mode=False):
    b64 = ascii_uppercase + ascii_lowercase + digits + '+/'

    block_size = block_size or _block_size(s)
    hashes = _spamsum(s, block_size, digest_len, legacy_mode)

    return ''.join(b64[h % 64] for h in hashes)


def main():
    path = argv[1]
    s = open(path).read()

    block_size = _block_size(s)

    while True:
        normal = spamsum(s, block_size, MAX_DIGEST_LEN)
        shorter = spamsum(s, block_size * 2, MAX_DIGEST_LEN / 2)

        normal_should_be_longer = len(normal) < (MAX_DIGEST_LEN / 2)
        can_reduce_block = block_size > MIN_BLOCK_SIZE

        if normal_should_be_longer and can_reduce_block:
            block_size /= 2
        else:
            print('%d:%s:%s' % (block_size, normal, shorter))
            return


if __name__ == '__main__':
    main()
