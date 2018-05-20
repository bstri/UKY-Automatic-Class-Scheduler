"""This file ensures that tests run by pytest will be able to access the code."""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))