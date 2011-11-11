#!/usr/bin/env python
from nose.tools import *
from elo.calculate import *

def setup():
  players = [{'name': 'A', 'score': 1200},
             {'name': 'B', 'score': 1000}]

def teardown():
  pass

def test_adjustment():
  adjustments = {
    (1,1,0.5): 0.5,
    (16, 1, 0.35993500019711494): 10.241039996846162,
    (32, 1, 0.0055919673088347787): 31.821057046117286,
    (64, 1, 0.75974692664795784): 15.376196694530698,
    (128, 1, 0.99900099900099915): 0.12787212787210933
  }
  for k, v in adjustments.iteritems():
    assert_equal(adjustment(*k), v)

def test_expectation():
  expectations = {
    (0, 0): 0.5,
    (0, 100): 0.35993500019711494,
    (100, 1000): 0.0055919673088347787,
    (1200, 1000): 0.75974692664795784,
    (1200, 0): 0.99900099900099915
  }
  for k, v in expectations.iteritems():
    assert_equal(expectation(*k), v)

def test_record_win():
  """ These wins must be played in order for the assertions to be valid"""
  record_win(players[0],players[1])
  assert_equal(players[0]['score'], 1016.0)
  assert_equal(players[1]['score'], 984.0)

  record_win(players[0],players[1])
  assert_equal(players[0]['score'], 1030.5304984710244)
  assert_equal(players[1]['score'], 969.46950152897546)

  record_win(players[1],players[0])
  assert_equal(players[0]['score'], 1011.7471336336108)
  assert_equal(players[1]['score'], 988.25286636638907)