#!/usr/bin/env python
from __future__ import division
from config import players, K, backup_file
from pprint import pprint
from os import system
from operator import itemgetter
from datetime import datetime

def expectation(ra, rb):
  """ Given rating a and rating b, compute the expectation, i.e. probability
      that a player with rating a will win against one with rating b. """
  return 1/(1 + 10**(-(ra-rb)/400))

def adjustment(k, outcome, expectation):
  """ Given k (elo volatility constant), the outcome (one of {-1,0,1} =
      {loss, draw, win} by player a), and the expectation (computed from the
      difference between the two players' scores), return the number of elo
      points the loser should award the winner. """
  return k*(outcome - expectation)

def record_win(player_a, player_b):
  """ Record a win by player with index a against the player with index b. """
  outcome = 1 # this means player_a won.

  ra = player_a['score']
  rb = player_b['score']
  expected = expectation(ra, rb)

  adj = adjustment(K, outcome, expected)
  player_a['score'] += adj
  player_b['score'] -= adj
  write_log_line(player_a, player_b)

def write_log_line(player_a, player_b):
  """ Write a csv log line recording the win.
      example:
      2011-11-11 12:00:12, won, Brandon Chinn, Justin Knoll, 1202.23, 1102.23
  """  
  pass

def won(a, b):
  print("%s defeated %s" % (players[a]['name'], players[b]['name']))
  resp = raw_input('Confirm (y/n): ')
  if resp[0].lower() == 'y':
    record_win(players[a], players[b])
  system('clear')
  ls()
  save()

def addplayer(name, initial_score):
  """ Add a new player with name and initial score to the ladder. """
  players.append({'name': name, 'score': initial_score})
  ls()

def save(file=backup_file):
  global players
  if len(players) == 0: 
    return
  
  outfile = open(file, 'w')
  players = sorted(players, key=itemgetter('score'), reverse=True)
  for i, p in enumerate(players):
    outfile.write("%s\t%f\n" % (p['name'].ljust(30), p['score']))
  outfile.close()

def restore(file=backup_file):
  infile = open(file, 'r')
  text = infile.readlines()
  infile.close()
  new_players = []
  for line in text:
    new_players.append({'name':line.split('\t')[0].strip(), 'score':float(line.split('\t')[1].strip())})
  
  if len(new_players) == 0:
    return

  global players
  players = new_players
  ls()

def ls():
  """ Output a current ladder """
  global players
  players = sorted(players, key=itemgetter('score'), reverse=True)
  system('clear')
  dateline()
  for i, p in enumerate(players):
      print("%d\t%s\t%.2f" % (i, p['name'].ljust(30), p['score']))
  helplines()

def dateline():
  """ Output a title line including the current date and time. """
  now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
  print "BitTorrent Pool Elo Ladder | %s" % now
  print "=================================================="

def helplines():
  """ Output a description of available commands. """
  print "=================================================="
  print "won(a,b) = player a wins against player b, e.g. won(1, 4)"
  print "addplayer(\"name\", initial_score) = add a new player with initial \
         score (recommend 1000)"

