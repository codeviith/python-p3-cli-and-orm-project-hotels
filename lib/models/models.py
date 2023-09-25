from models.__init__ import CONN, CURSOR

# Hotel model
class Hotel:

    all = []

    def __init__(self, name):
        self.id = None
        self.name = name
        self.reviews = []

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
        hotels = [hotel for hotel in Hotel.all if hotel.id == id]

        if hotels:
            return hotels[0]
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
        
        # Remove the hotel instance from Hotel.all
        Hotel.all = [hotel for hotel in Hotel.all if hotel.id != self.id]

        # Delete the associated reviews from the database and remove the associated review instances from Review.all
        # The idea here is that there should not exist reviews for a hotel that no longer exists
        for review in self.reviews:
            if review.hotel_id == self.id:
                review.delete()

# Review model
class Review:

    all = []

    def __init__(self, hotel_id, rating):
        self.id = None
        self.hotel_id = hotel_id
        self.hotel = Hotel.find_by_id(hotel_id)
        self.hotel.reviews.append(self)
        self.rating = rating

    @property
    def hotel(self):
        return self._hotel
    
    @hotel.setter
    def hotel(self, hotel_parameter):
        if isinstance(hotel_parameter, Hotel):
            self._hotel = hotel_parameter
        else:
            raise Exception(f"Error: Hotel # {self.hotel_id} does not exist!")
        
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, rating_parameter):
        if 1 <= rating_parameter <= 5:
            self._rating = rating_parameter
        else:
            raise Exception("Error: Rating must be between 1 and 5!")

    def __repr__(self):
        return f'Review # {self.id}: {self.hotel.name} received a rating of {self.rating}'

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                hotel_id INTEGER,
                rating INTEGER
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS reviews
        """

        CURSOR.execute(sql)
        
        cls.all = []

    @classmethod
    def new_from_db(cls, row):
        review = cls(row[1], row[2])
        review.id = row[0]
        return review
    
    # Read - Get all reviews
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM reviews
        """

        all = CURSOR.execute(sql).fetchall()
        
        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all
    
    # Read - Find review by id
    @classmethod
    def find_by_id(cls, id):
        reviews = [review for review in Review.all if review.id == id]

        if reviews:
            return reviews[0]
        else:
            return None

    # Create - Create new review
    @classmethod
    def create(cls, hotel_id, rating):
        review = Review(hotel_id, rating)
        review.save()
        cls.all.append(review)
        return review
    
    def save(self):
        sql = """
            INSERT INTO reviews (hotel_id, rating)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.hotel_id, self.rating))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM reviews").fetchone()[0]
        CONN.commit()

    # Update - Update a review
    def update(self):
        sql = """
            UPDATE reviews
            SET hotel_id = ?, rating = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.hotel_id, self.rating, self.id))
        CONN.commit()

    # Delete - Delete a review
    def delete(self):
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
        # Remove the review instance from Review.all
        Review.all = [review for review in Review.all if review.id != self.id]

        # Remove the review instance from the associated hotel's reviews list
        self.hotel.reviews = [review for review in self.hotel.reviews if review.id != self.id]