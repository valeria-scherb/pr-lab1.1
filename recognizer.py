#!/usr/bin/env python
"""
Image recognition class
"""

import random as r
import math


class Recognizer:
    def __init__(self):
        self.gks = {}
        self.n = self.m = 0
        self.p = self.q = None
        self.ln_p = self.ln_q = None

    def set_size(self, n, m):
        self.n = n
        self.m = m

    def set_noise_prob(self, p):
        very_large_number = 10 ** 20
        self.p = p
        self.q = 1.0 - p
        try:
            self.ln_p = math.log(p)
        except ValueError:
            self.ln_p = -very_large_number
        try:
            self.ln_q = math.log(1.0 - p)
        except ValueError:
            self.ln_q = -very_large_number

    def remember(self, k, g_x):
        self.gks[k] = g_x

    def recognize(self, x):
        key = 0
        value = -math.inf
        for k in self.gks.keys():
            gk = self.gks[k]
            summa = 0
            for i in range(0, self.n):
                for j in range(0, self.m):
                    summa += x[i][j] ^ gk[i][j]
            add = (self.ln_p - self.ln_q) * summa + self.ln_q * self.n * self.m
            if add > value:
                key = k
                value = add
        return key

    def testing_generate_image(self, k, seed=None):
        if seed is not None:
            r.seed(seed)
        gk = []
        for i in range(0, self.n):
            gk.append(r.choices([0, 1], k=self.m))
        self.gks[k] = gk

    def testing_generate_input(self, k, seed=None):
        if seed is not None:
            r.seed(seed)
        gk = self.gks[k]
        x = []
        for i in range(0, self.n):
            n = r.choices([0, 1], [self.q, self.p], k=self.m)
            x.append([a ^ b for a, b in zip(gk[i], n)])
        return x
