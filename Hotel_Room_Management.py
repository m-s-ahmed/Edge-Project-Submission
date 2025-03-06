import datetime

class Room:
    def __init__(self, room_number, room_type, price, amenities):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.amenities = amenities
        self.is_booked = False

    def __repr__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"Room {self.room_number}: {self.room_type}, Price: ${self.price}, Status: {status}, Amenities: {', '.join(self.amenities)}"


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = {}

    def add_room(self, room):
        if room.room_number in self.rooms:
            print(f"Room {room.room_number} already exists!")
        else:
            self.rooms[room.room_number] = room
            #print(f"Room {room.room_number} added successfully!")

    def delete_room(self, room_number):
        if room_number in self.rooms:
            del self.rooms[room_number]
            print(f"Room {room_number} deleted successfully!")
        else:
            print("Room not found!")

    def get_available_rooms(self):
        return [room for room in self.rooms.values() if not room.is_booked]


class Customer:
    def __init__(self, budget, preferred_room_type, required_amenities):
        self.budget = budget
        self.preferred_room_type = preferred_room_type
        self.required_amenities = required_amenities

    def filter_rooms(self, rooms):
        return [
            room for room in rooms
            if room.price <= self.budget
            and (self.preferred_room_type.lower() in room.room_type.lower() or not self.preferred_room_type)
            and all(amenity in room.amenities for amenity in self.required_amenities)
        ]

    def generate_receipt(self, room):
        print("\n--- Booking Receipt ---")
        print(f"Hotel: {hotel.name}")
        print(f"Room Number: {room.room_number}")
        print(f"Room Type: {room.room_type}")
        print(f"Price: ${room.price}")
        print(f"Amenities: {', '.join(room.amenities)}")
        print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-------------------------\n")

    def offer_room(self, hotel):
        available_rooms = hotel.get_available_rooms()
        filtered_rooms = self.filter_rooms(available_rooms)

        if not filtered_rooms:
            print("\nNo rooms match your criteria. Please adjust your preferences.")
            return

        print("\nMatching Rooms:")
        for room in filtered_rooms:
            print(room)

        choice = input("\nWould you like to book any room? (Yes/No): ").strip().lower()
        if choice == 'yes':
            try:
                room_number = int(input("Enter Room Number to Book: "))
                if room_number in [room.room_number for room in filtered_rooms]:
                    hotel.rooms[room_number].is_booked = True
                    print(f"Room {room_number} successfully booked!")
                    self.generate_receipt(hotel.rooms[room_number])
                else:
                    print("Invalid Room Number or Room Already Booked!")
            except ValueError:
                print("Invalid Input! Please enter a valid room number.")


def admin_panel(hotel):
    admin_id = "admin"
    admin_password = "password"

    entered_id = input("Enter Admin ID: ")
    entered_password = input("Enter Admin Password: ")
    if entered_id == admin_id and entered_password == admin_password:
        print("Access Granted!")
        while True:
            admin_option = input("Choose option: Add Room or Delete Room (Add/Delete/Exit): ").strip().lower()
            if admin_option == 'add':
                try:
                    room_number = int(input("Enter Room Number: "))
                    room_type = input("Enter Room Type: ")
                    price = float(input("Enter Price: $"))
                    amenities = input("Enter Amenities (comma separated): ").split(",")
                    amenities = [amenity.strip() for amenity in amenities if amenity.strip()]
                    hotel.add_room(Room(room_number, room_type, price, amenities))
                except ValueError:
                    print("Invalid input! Please enter valid details.")

            elif admin_option == 'delete':
                try:
                    room_number = int(input("Enter Room Number to Delete: "))
                    hotel.delete_room(room_number)
                except ValueError:
                    print("Invalid input! Please enter a valid room number.")

            elif admin_option == 'exit':
                break

            else:
                print("Invalid option!")
    else:
        print("Access Denied! Invalid ID or Password.")


# Create Hotel Object
hotel = Hotel("Ocean View Hotel")

# Add Rooms
hotel.add_room(Room(101, "Single", 100, ["Wi-Fi", "Air Conditioning", "TV"]))
hotel.add_room(Room(102, "Double", 150, ["Wi-Fi", "Air Conditioning", "TV", "Minibar"]))
hotel.add_room(Room(103, "Suite", 250, ["Wi-Fi", "Air Conditioning", "TV", "Minibar", "Ocean View"]))
hotel.add_room(Room(104, "Single", 90, ["Wi-Fi", "TV"]))
hotel.add_room(Room(105, "Double", 200, ["Wi-Fi", "Air Conditioning", "TV", "Minibar", "Balcony"]))

while True:
    print("\nWelcome to the hotel! Please select an option:")
    user_choice = input("1. Booking Panel\n2. Admin Panel\n3. Exit\nEnter your choice (1/2/3): ").strip()

    if user_choice == '1':  # Booking Panel
        try:
            budget = float(input("Enter your budget (in USD): $"))
            preferred_room_type = input("Enter your preferred room type (Single, Double, Suite, or leave blank for any): ")
            required_amenities = input("Enter the amenities you require (comma separated, e.g., Wi-Fi, TV): ").split(",")
            required_amenities = [amenity.strip() for amenity in required_amenities if amenity.strip()]

            customer = Customer(budget, preferred_room_type, required_amenities)
            customer.offer_room(hotel)
        except ValueError:
            print("Invalid input! Please enter valid numbers for budget.")

    elif user_choice == '2':  # Admin Panel
        admin_panel(hotel)

    elif user_choice == '3':  # Exit
        print("Thank you for using our hotel booking system!")
        break

    else:
        print("Invalid choice! Please select 1 for Booking Panel, 2 for Admin Panel, or 3 to Exit.")
