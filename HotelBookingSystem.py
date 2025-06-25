# Hotel-Booking-System
from datetime import datetime

def save_to_file(data):
    """Save customer data to a file."""
    with open("customers.txt", "a") as file:
        file.write(data + "\n")

def read_from_file():
    """Read customer data from file."""
    customers = []
    try:
        with open("customers.txt", "r") as file:
            customers = file.readlines()
    except FileNotFoundError:
        pass
    return customers

class Customer:
    def _init_(self, name, phone, room_type, room_number, check_in, check_out):
        self.name = name
        self.phone = phone
        self.room_type = room_type
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _str_(self):
        return (f"{self.name} | Phone: {self.phone} | {self.room_type} Room {self.room_number} | "
                f"{self.check_in} to {self.check_out} | Booked on {self.booking_date}")

class Hotel:
    def _init_(self):
        self.customers = []
        self.rooms = {
            'Single': [101, 102, 103, 104, 105],
            'Double': [201, 202, 203, 204, 205],
            'Suite': [301, 302, 303]
        }
        self.occupied_rooms = {
            'Single': {},
            'Double': {},
            'Suite': {}
        }

    def add_customer(self, customer):
        """Add a new customer and mark the room as occupied."""
        self.customers.append(customer)
        save_to_file(str(customer))

        # Mark the room as occupied
        room_schedule = self.occupied_rooms[customer.room_type]
        if customer.room_number not in room_schedule:
            room_schedule[customer.room_number] = []
        room_schedule[customer.room_number].append((customer.check_in, customer.check_out))

    def view_customers(self):
        """View all customers."""
        customers = read_from_file()
        if customers:
            for customer in customers:
                print(customer.strip())
        else:
            print("No customers found.")

    def get_available_rooms(self, room_type, check_in, check_out):
        """Get available rooms for the specified type and dates."""
        check_in = datetime.strptime(check_in, "%Y-%m-%d")
        check_out = datetime.strptime(check_out, "%Y-%m-%d")
        available_rooms = []

        for room in self.rooms[room_type]:
            if room not in self.occupied_rooms[room_type]:
                available_rooms.append(room)
            else:
                # Check if the room is available for the given dates
                is_available = True
                for booked_in, booked_out in self.occupied_rooms[room_type][room]:
                    booked_in = datetime.strptime(booked_in, "%Y-%m-%d")
                    booked_out = datetime.strptime(booked_out, "%Y-%m-%d")
                    if not (check_out <= booked_in or check_in >= booked_out):
                        is_available = False
                        break
                if is_available:
                    available_rooms.append(room)
        
        return available_rooms

def display_menu():
    """Display menu options for the user."""
    print("\nHotel Booking System")
    print("1. Book a Room")
    print("2. View All Customers")
    print("3. Exit")

def book_room(hotel):
    """Book a room for a customer."""
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    
    room_type = input("Choose a room type (Single/Double/Suite): ").capitalize()
    if room_type not in ['Single', 'Double', 'Suite']:
        print("Invalid room type. Please try again.")
        return

    # Display available rooms
    print(f"Available {room_type} rooms:")
    for room in hotel.rooms[room_type]:
        print(f"- {room}")

    room_number = int(input("Choose a room number from the list above: "))
    if room_number not in hotel.rooms[room_type]:
        print("Invalid room number. Please try again.")
        return

    check_in = input("Enter check-in date (YYYY-MM-DD): ")
    check_out = input("Enter check-out date (YYYY-MM-DD): ")
    try:
        # Validate date format
        datetime.strptime(check_in, "%Y-%m-%d")
        datetime.strptime(check_out, "%Y-%m-%d")
        if datetime.strptime(check_in, "%Y-%m-%d") >= datetime.strptime(check_out, "%Y-%m-%d"):
            print("Check-out date must be after check-in date.")
            return
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check room availability
    available_rooms = hotel.get_available_rooms(room_type, check_in, check_out)
    if room_number not in available_rooms:
        print(f"Room {room_number} is not available for the selected dates.")
        return

    customer = Customer(name, phone, room_type, room_number, check_in, check_out)
    hotel.add_customer(customer)
    print(f"Booking successful for {name} in Room {room_number}!")

def main():
    """Main function to run the hotel booking system."""
    hotel = Hotel()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            book_room(hotel)
        elif choice == "2":
            hotel.view_customers()
        elif choice == "3":
            print("Thank you for using the Hotel Booking System!")
            break
        else:
            print("Invalid choice, please try again.")

if _name_ == "_main_":
    main()
