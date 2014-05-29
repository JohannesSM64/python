#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yatzy implemented in Python.
"""
# Written by Johannes Langøy, 2014. Public domain.

def numfunc(dice, n):
    amt = dice.count(n)
    if amt >= 1:
        return amt * n

def amtfunc(dice, n):
    for i in reversed(range(1,7)):
        if dice.count(i) >= n:
            return i * n

def ones(dice): return numfunc(dice, 1)
def twos(dice): return numfunc(dice, 2)
def threes(dice): return numfunc(dice, 3)
def fours(dice): return numfunc(dice, 4)
def fives(dice): return numfunc(dice, 5)
def sixes(dice): return numfunc(dice, 6)

def one_pair(dice): return amtfunc(dice, 2)
def two_pairs(dice):
    saved = None
    for i in reversed(range(1,7)):
        if dice.count(i) == 2:
            if saved:
                return (saved*2) + (i*2)
            else:
                saved = i
def three_of_a_kind(dice): return amtfunc(dice, 3)
def four_of_a_kind(dice): return amtfunc(dice, 4)
def small_straight(dice):
    for i in range(1,6):
        if dice.count(i) == 0:
            return None
    return 15
def large_straight(dice):
    for i in range(2,7):
        if dice.count(i) == 0:
            return None
    return 20
def full_house(dice):
    two_of = None
    three_of = None
    for i in reversed(range(1,7)):
        amt = dice.count(i)
        if amt == 2:
            two_of = i
        elif amt == 3:
            three_of = i
        if two_of and three_of:
            return (two_of*2) + (three_of*3)

def yatzy(dice):
    for i in dice:
        if i != dice[0]:
            return None
    return 50

goals = {
    "Ones": ones,
    "Twos": twos,
    "Threes": threes,
    "Fours": fours,
    "Fives": fives,
    "Sixes": sixes,
    "One pair": one_pair,
    "Two pairs": two_pairs,
    "Three of a kind": three_of_a_kind,
    "Four of a kind": four_of_a_kind,
    "Small straight": small_straight,
    "Large straight": large_straight,
    "Full house": full_house,
    "Chance": sum,
    "Yatzy": yatzy
}
