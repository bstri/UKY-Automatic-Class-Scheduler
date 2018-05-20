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