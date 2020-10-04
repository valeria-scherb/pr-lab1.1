#!/usr/bin/env python
"""
Unit tests for Image recognition class
"""

import unittest
import recognizer


class TestRecognizer(unittest.TestCase):

    def noise_checker(self, p, sz=10, nk=10, ni=10):
        r = recognizer.Recognizer()
        r.set_size(sz, sz)
        r.set_noise_prob(p)
        for i in range(0, nk):
            r.testing_generate_image(i, 2020000 + i)
        ok = 0
        for i in range(0, nk):
            for n in range(0, ni):
                x = r.testing_generate_input(i, 2222000 + i*100 + n)
                a = r.recognize(x)
                if a == i:
                    ok += 1
        return ok

    def test_low_noises(self):
        assert self.noise_checker(0.1) == 100
        assert self.noise_checker(0.2) == 100
        assert self.noise_checker(0.8) == 100
        assert self.noise_checker(0.9) == 100

    def test_medium_noises(self):
        assert self.noise_checker(0.3) >= 95
        assert self.noise_checker(0.7) >= 95

    def test_high_noises(self):
        assert self.noise_checker(0.35) >= 80
        assert self.noise_checker(0.65) >= 80

    def test_highest_noises(self):
        assert self.noise_checker(0.4) >= 50
        assert self.noise_checker(0.6) >= 50


if __name__ == '__main__':
    unittest.main()
