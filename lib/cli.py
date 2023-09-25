#!/usr/bin/env python3
# lib/cli.py

from helpers import (
    exit_program,
    initialize,
    create_hotel,
    get_all_hotels,
    get_hotel_by_id,
    update_hotel,
    delete_hotel
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice in ["c", "C"]:
            create_hotel()
        elif choice in ["r", "R"]:
            get_all_hotels()
        elif choice in ["r1", "R1"]:
            get_hotel_by_id()
        elif choice in ["u", "U"]:
            update_hotel()
        elif choice in ["d", "D"]:
            delete_hotel()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0 - Exit the program")
    print("C - Create a new hotel")
    print("R - Get all hotel info")
    print("R1 - Get info for 1 hotel")
    print("U - Update a hotel")
    print("D - Delete a hotel")


if __name__ == "__main__":
    initialize()
    main()