import sys
import os

dirname, filename = os.path.split(os.path.abspath( __file__))
os.path.realpath(__file__)
print(dirname)
print(filename)