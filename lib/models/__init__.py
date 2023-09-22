import sqlite3

CONN = sqlite3.connect('hotels.db')
CURSOR = CONN.cursor()
