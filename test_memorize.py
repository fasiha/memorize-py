import memorizesrs
import unittest

from math import exp, sqrt, inf, isfinite
from random import Random


def tcToRecall(timeconstant):
  return lambda t: exp(-t * abs(timeconstant))


def mean(v):
  return sum(v) / len(v)


def isSorted(v, key=lambda x, y: x < y):
  return all(key(v[i], v[i + 1]) for i in range(len(v) - 1))


class TestMemorize(unittest.TestCase):

  def test_q_parameter(self):
    N = 10000
    T = inf
    qs = [1e-2, 1e-1, 1e0, 1e1, 1e2]
    timeConstants = [1e-2, 1e-1, 1e0, 1e1, 1e3]

    outer = []
    for q in qs:
      smallestRate = sqrt(q)
      means = []
      for tc in timeConstants:
        rng = Random(123)
        recall = tcToRecall(tc)
        res = [memorizesrs.schedule(recall, q, T, rng=rng) for i in range(N)]
        self.assertTrue(all(map(isfinite, res)), 'no infs for T=inf')
        means.append(mean(res))

      # print(means)
      self.assertTrue(isSorted(means, lambda hi, lo: hi > lo), 'mean time decreases with pRecall')
      self.assertLess(means[-1], smallestRate * 1.02,
                      'super-low-recall rate very close to smallest rate')

      outer.append(means)

    for (tci, tc) in enumerate(timeConstants):
      increasingQ = []
      for (qi, q) in enumerate(qs):
        increasingQ.append(outer[qi][tci])
      self.assertTrue(isSorted(increasingQ, lambda lo, hi: lo < hi), 'higher q -> later reviews')

  def test_noninf_T(self):
    N = 10000
    rng = Random(123)
    recall = tcToRecall(1.)
    T = 1.0
    qs = [1e-2, 1e-1, 1e0, 1e1, 1e2]
    finiteRatios = ([
        mean([isfinite(memorizesrs.schedule(recall, q, T, rng=rng)) for i in range(N)]) for q in qs
    ])
    self.assertTrue(isSorted(finiteRatios, lambda hi, lo: hi > lo), msg='q+, infs+')
