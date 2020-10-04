#!/usr/bin/env python

class Recognizer:
    def __init__(self):
        self.gks = {}
        self.n = self.m = 0
        self.p = 0.0
        self.q = 1.0

    def set_size(self, n, m):
        self.n = n
        self.m = m

    def set_noise_prob(self, p):
        self.p = p
        self.q = 1.0 - p

    def remember(self, k, g_x):
        self.gks[k] = g_x

    def recognize(self, x):
        key = 0
        value = 0
        for k in self.gks.keys():
            gk = self.gks[k]
            mul = 1
            for i in range(0, self.n):
                for j in range(0, self.m):
                    mul *= self.p ** (x[i][j] ^ gk[i][j])
                    mul *= self.q ** (1 ^ x[i][j] ^ gk[i][j])
            if mul > value:
                key = k
                value = mul
        return key
