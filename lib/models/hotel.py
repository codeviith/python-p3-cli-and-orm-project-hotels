from models.__init__ import CONN, CURSOR

class Hotel:

    all = []

    def __init__(self, name):
        self.id = None
        self.name = name

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id_parameter):
        if (not hasattr(self, 'id')) or (self.id == None):
            self._id = id_parameter

    def __repr__(self):
        return f'Hotel # {self.id}: {self.name}'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS hotels
        """

        CURSOR.execute(sql)
        
        cls.all = []

    @classmethod
    def new_from_db(cls, row):
        hotel = cls(row[1])
        hotel.id = row[0]
        return hotel
    
    # Read - Get all hotels
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM hotels
        """

        all = CURSOR.execute(sql).fetchall()
        
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all
    
    # Read - Find hotel by id
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM hotels
            WHERE hotels.id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()

        if row:
            return cls.new_from_db(row)
        else:
            return None

    # Create - Create new hotel
    @classmethod
    def create(cls, name):
        hotel = Hotel(name)
        hotel.save()
        cls.all.append(hotel)
        return hotel
    
    def save(self):
        sql = """
            INSERT INTO hotels (name)
            VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM hotels").fetchone()[0]
        CONN.commit()

    # Update - Update a hotel
    def update(self):
        sql = """
            UPDATE hotels
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    # Delete - Delete a hotel
    def delete(self):
        sql = """
            DELETE FROM hotels
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
        Hotel.all = list(filter(lambda h: h.id != self.id, Hotel.all))