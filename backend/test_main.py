import pytest
import sqlite3
from main import DataProcessing

dp = None
def setup_module(module):
    global dp
    dp = DataProcessing()

def teardown_module(module):
    global dp
    del dp

def test_avg():
    assert dp.avg("Polska", "2010") == 366623.0
    assert dp.avg("Polska", "2010", "a") == "Gender should be 'm' or 'f'"
    assert dp.avg("Polska", "2010", "m") == 160988.0
    assert dp.avg("Polska", 2011) == 355223.5
    assert dp.avg("Polska", "2012", "f") == 194390.66666666666
    assert dp.avg("Polska", "2013") == 338737.5
    assert dp.avg("Polska", "2014") == 329784.8
    assert dp.avg("Polska", "2015") == 320748.6666666667
    assert dp.avg("Polska", "2016") == 311837.71428571426
    assert dp.avg("Polska", "2017") == 305111.75
    assert dp.avg("Polska", "2018") == 298748.22222222225
    assert dp.avg("Niemcy", "2017") == "Voivodeship not recognized"
    assert dp.avg("Małopolskie", "2019") == "Year should be between 2010 and 2018"
    
def test_passed():
    assert dp.passed("Polska") == None
    assert dp.passed("Niemcy") == "Voivodeship not recognized"
    assert dp.passed(-1) == "Voivodeship not recognized"
    assert dp.passed("Polska", "m") == None
    assert dp.passed("Polska", "a") == "Gender should be 'm' or 'f'"

def test_best():
    assert dp.best("2010") == "Mazowieckie"
    assert dp.best("2011", "f") == "Mazowieckie"
    assert dp.best("2012", "m") == "Mazowieckie"
    assert dp.best("2013", "a") == "Gender should be 'm' or 'f'"
    assert dp.best("2019") == "Year should be between 2010 and 2018"
    assert dp.best(2015) == "Mazowieckie"
    assert dp.best("2017") == "Mazowieckie"
    assert dp.best("2018") == "Mazowieckie"

def test_regress():
    assert dp.regress() == None
    assert dp.regress("m") == None
    assert dp.regress("f") == None
    assert dp.regress("a") == "Gender should be 'm' or 'f'"

def test_compare():
    assert dp.compare("Małopolskie", "Podkarpackie") == None
    assert dp.compare("Małopolskie", "Podkarpackie", "m") == None
    assert dp.compare("Małopolskie", "Podkarpackie", "f") == None
    assert dp.compare("Małopolskie", "Podkarpackie", "a") == "Gender should be 'm' or 'f'"
    assert dp.compare("Niemcy", "Podkarpackie") == "Voivodeship 1 not recognized"
    assert dp.compare("Małopolskie", "Litwa") == "Voivodeship 2 not recognized"
    assert dp.compare("Chorwacja", "Litwa") == "Voivodeship 1 not recognized"
    assert dp.compare("Chorwacja", "Litwa", "m") == "Voivodeship 1 not recognized"
