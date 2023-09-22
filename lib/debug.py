#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.hotel import Hotel
import ipdb

def reset_database():
    Hotel.drop_table()
    Hotel.create_table()

ipdb.set_trace()
