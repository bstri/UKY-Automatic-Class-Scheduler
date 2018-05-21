import pytest
import tkinter as tk
from Entry import *

def setup_module():
	global master
	master = tk.Tk()

def make(cls, *args, **kwargs): # decorator maker
	def new(func): # new decorator
		def call():
			obj = cls(master, *args, **kwargs)
			try:
				func(obj)
			finally:
				obj.destroy()
		return call
	return new

@make(Entry, text="Hi!")
def test_Entry(obj):
	assert obj.text == "Hi!"

@make(Entry, text="Hi!")
def test_EntrySet(obj):
	obj.text = "Second"
	assert obj.text == "Second"

@make(EntryLetters)
def test_EntryLetters(obj):
	assert obj.validate("Sample")

@make(EntryLetters)
def test_EntryLettersEmpty(obj):
	assert obj.validate("")

@make(EntryLetters)
def test_EntryLettersNoNumbers(obj):
	assert not obj.validate("With123s")

@make(EntryNumbers)
def test_EntryNumbers(obj):
	assert obj.validate("502")

@make(EntryNumbers)
def test_EntryNumbersNoNumbers(obj):
	assert not obj.validate("3Text")

@make(EntryRange)
def test_EntryRangeValidates(obj):
	assert obj.validate("1, 2, 4-6")

@make(EntryRange)
def test_EntryRangeNoNumbers(obj):
	assert not obj.validate("1, hi")

@make(EntryRange)
def test_EntryRangeGetRange(obj):
	obj.text = "1, 4-6"
	assert obj.GetRange() == [1, 4, 5, 6]

@make(EntryRange)
def test_EntryRangeGetRangeOverlap(obj):
	obj.text = "1, 5, 4-6"
	assert obj.GetRange() == [1, 4, 5, 6]

@make(EntryRange)
def test_EntryRangeGetRangeOutOfOrder(obj):
	obj.text = "3, 1, 9"
	assert obj.GetRange() == [1, 3, 9]

@make(EntryRange, maxNum=10)
def test_EntryRangeGetRangeNumTooLarge(obj):
	with pytest.raises(ValueError):
		obj.text = "1, 5-15"
		obj.GetRange()
