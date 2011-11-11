#!/usr/bin/env python
from __future__ import division
from config import *
from pprint import pprint
from os import system
from operator import itemgetter
from datetime import datetime

def expectation(ra, rb):
  return 1/(1 + 10**(-(ra-rb)/400))

def adjustment(k, outcome, expected):
  return k*(outcome - expected)

def won(a, b):
  outcome = 1 # this means player_a won.
  player_a = players[a]
  player_b = players[b]

  ra = player_a['score']
  rb = player_b['score']
  expected = expectation(ra, rb)

  adj = adjustment(K, outcome, expected)
  player_a['score'] += adj
  player_b['score'] -= adj
  system('clear')
  ls()

def ls():
  global players
  players = sorted(players, key=itemgetter('score'), reverse=True)
  system('clear')
  dateline()
  for i, p in enumerate(players):
      print("%d\t%s\t%.2f" % (i, p['name'].ljust(30), p['score']))
  helplines()

def dateline():
  print "BitTorrent Pool Elo Ladder | %s" % datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
  print "=================================================="

def helplines():
  print "=================================================="
  print "won(a,b) = player a wins against player b, e.g. won(1, 4)"
  print "addplayer(\"name\", initial_score) = add a new player with initial score (recommend 1000)"

def addplayer(name, initial_score):
  global players
  players.append({'name': name, 'score': initial_score})
  ls()

ls()

