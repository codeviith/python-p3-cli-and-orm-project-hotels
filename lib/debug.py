#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.models import Hotel, Review
import ipdb

def reset_database():
    Hotel.drop_table()
    Review.drop_table()
    Hotel.create_table()
    Review.create_table()

ipdb.set_trace()
