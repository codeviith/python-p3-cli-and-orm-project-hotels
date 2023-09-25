# lib/helpers.py

from models.models import Hotel, Review

def initialize():
    Hotel.create_table()
    Hotel.get_all()
    Review.create_table()
    Review.get_all()

def create_hotel():
    print("Enter the name for your new hotel:")
    hotel_name = input("> ")
    while not hotel_name:
        print("Error: Name cannot be blank!")
        print("Enter the name for your new hotel:")
        hotel_name = input("> ")
    new_hotel = Hotel.create(hotel_name)
    print("Hotel successfully added!")
    print(new_hotel)
    keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def get_all_hotels():
    if len(Hotel.all) == 0:
        print("Error: There are no hotels in the database!")
    else:
        for hotel in Hotel.all:
            print(hotel)
        print("Successfully retrieved all hotel data!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def get_hotel_by_id():
    if len(Hotel.all) == 0:
        print("Error: There are no hotels in the database!")
    else:
        hotel = search_by_id('find')
        print(hotel)
        print("Successfully retrieved hotel data!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def update_hotel():
    if len(Hotel.all) == 0:
        print("Error: There are no hotels in the database!")
    else:
        hotel = search_by_id('update')
        print("Enter the new name for the hotel:")
        hotel_name = input("> ")
        while not hotel_name:
            print("Error: Name cannot be blank!")
            print("Enter the new name for the hotel:")
            hotel_name = input("> ")
        hotel.name = hotel_name
        hotel.update()
        print(hotel)
        print("Successfully updated hotel data!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def delete_hotel():
    if len(Hotel.all) == 0:
        print("Error: There are no hotels in the database!")
    else:
        hotel = search_by_id('delete')
        hotel.delete()
        print(f"Successfully deleted hotel!")
        keyboard_input = input("* Press any key and then press 'return' to continue *\n")

def search_by_id(word):
    print(f"Enter the id for the hotel you want to {word}:")
    id = input("> ")
    
    if id.isdigit():
        hotel = Hotel.find_by_id(int(id))
    else:
        hotel = None
    
    while not hotel:
        print("Error: Hotel not found!")
        print(f"Enter the id for the hotel you want to {word}:")
        id = input("> ")

        if id.isdigit():
            hotel = Hotel.find_by_id(int(id))
        else:
            hotel = None

    return hotel

def exit_program():
    print("Goodbye!")
    exit()
