import os
from datetime import datetime, date
import re

# Define a custom delimiter that is unlikely to appear in user input
BOOKING_DELIMITER = "|||" 
FIELD_DELIMITER = "@@" 

class CarWashCLIApp:
    def __init__(self):
        # File to store bookings
        self.bookings_file = "car_wash_bookings.txt"
        self.packages = {
            "Basic Wash": 299,
            "Premium Wash": 499,
            "Deluxe Detail": 799
        }
        self.bookings = self.load_bookings()
        # Determine the next booking ID
        self.next_booking_id = max([b['booking_id'] for b in self.bookings] or [0]) + 1

    def load_bookings(self):
        """Load bookings from the delimited text file."""
        bookings = []
        if os.path.exists(self.bookings_file):
            try:
                with open(self.bookings_file, 'r') as f:
                    content = f.read()
                
                # Split content into individual booking records
                records = content.strip().split(BOOKING_DELIMITER)
                
                for record in records:
                    if not record.strip():
                        continue

                    fields = record.strip().split(FIELD_DELIMITER)
                    
                    # Ensure the record has the expected number of fields (8 fields)
                    if len(fields) == 8:
                        try:
                            booking = {
                                "booking_id": int(fields[0]),
                                "name": fields[1],
                                "phone": fields[2],
                                "address": fields[3],
                                "package": fields[4],
                                "date": fields[5],
                                "time": fields[6],
                                "notes": fields[7],
                                "booked_on": "" # Booked_on is not strictly needed for reload logic
                            }
                            bookings.append(booking)
                        except ValueError:
                            # Skip malformed record if ID conversion fails
                            continue

            except IOError:
                print("⚠️ Warning: Could not read existing bookings file. Starting fresh.")
                return []
        return bookings

    def save_bookings(self):
        """Save bookings to the delimited text file."""
        try:
            with open(self.bookings_file, 'w') as f:
                records = []
                for booking in self.bookings:
                    # Construct the delimited string for one booking
                    record = FIELD_DELIMITER.join([
                        str(booking['booking_id']),
                        booking['name'],
                        booking['phone'],
                        booking['address'],
                        booking['package'],
                        booking['date'],
                        booking['time'],
                        booking['notes']
                    ])
                    records.append(record)
                
                # Join all booking records with the primary delimiter
                f.write(BOOKING_DELIMITER.join(records) + BOOKING_DELIMITER)
                
        except IOError:
            print("❌ Error: Could not save bookings to file.")

    def run(self):
        """Main application loop."""
        print("=" * 40)
        print("🎯 Dust Heist - Doorstep Car Wash Service")
        print("We Are Here to Heist All the Dust!")
        print("=" * 40)

        while True:
            self.display_menu()
            choice = input("Enter your choice (1-4): ").strip()
            print("-" * 40)

            if choice == '1':
                self.book_service()
            elif choice == '2':
                self.view_packages()
            elif choice == '3':
                self.view_bookings()
            elif choice == '4':
                print("👋 Thank you for using Dust Heist. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1, 2, 3, or 4.")

            input("\nPress ENTER to continue...")
            print("-" * 40)

    def display_menu(self):
        """Prints the main menu options."""
        print("\n--- Main Menu ---")
        print("1. 📅 Book a Service")
        print("2. 🔍 View Our Packages")
        print("3. 📜 View All Bookings")
        print("4. 🚪 Exit")

    # --- Utility Functions ---

    def get_valid_input(self, prompt, validation_func=None, error_msg="Invalid input. Please try again."):
        """Helper function to get and validate user input."""
        while True:
            user_input = input(prompt).strip()
            if user_input and (validation_func is None or validation_func(user_input)):
                return user_input
            print(f"** {error_msg} **")

    def validate_phone(self, phone):
        """Validates if the phone number is 10-15 digits long."""
        return re.match(r'^\d{10,15}$', phone) is not None

    def validate_date_time(self, date_str, time_str):
        """Validates the date and time strings and checks if it's in the future."""
        try:
            booking_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            if booking_datetime < datetime.now():
                print("   Booking date/time must be in the future.")
                return None
            return booking_datetime
        except ValueError:
            print("   Date format must be YYYY-MM-DD and time format HH:MM (24-hour).")
            return None

    # --- Core Application Logic ---

    def book_service(self):
        """Collects details and processes a new booking."""
        print("\n--- Book Your Service ---")
        
        # 1. Collect Customer Details
        name = self.get_valid_input("Customer Name: ", lambda x: len(x) > 0, "Name cannot be empty.")
        phone = self.get_valid_input("Phone Number (10-15 digits): ", self.validate_phone, "Phone number must be 10 to 15 digits.")
        address = self.get_valid_input("Address: ", lambda x: len(x) > 5, "Address must be at least 5 characters long.")
        
        # 2. Package Selection
        self.view_packages()
        package_names = list(self.packages.keys())
        pkg_prompt = "Select Package Number (1, 2, or 3): "
        
        while True:
            pkg_choice = input(pkg_prompt).strip()
            try:
                pkg_index = int(pkg_choice) - 1
                if 0 <= pkg_index < len(package_names):
                    package_name = package_names[pkg_index]
                    package_info = f"{package_name} - ₹{self.packages[package_name]}"
                    break
                else:
                    print("** Invalid package number. Please enter 1, 2, or 3. **")
            except ValueError:
                print("** Invalid input. Please enter a number. **")

        # 3. Date and Time Selection
        while True:
            print(f"\nCurrent Date: {date.today().strftime('%Y-%m-%d')}")
            date_str = self.get_valid_input("Date (YYYY-MM-DD): ")
            time_str = self.get_valid_input("Time (HH:MM 24hr format, e.g., 14:30): ")
            
            booking_dt = self.validate_date_time(date_str, time_str)
            if booking_dt:
                break
        
        notes = input("Additional Notes (Optional, press ENTER to skip): ").strip()
        # Use N/A placeholder to prevent empty fields in the text file
        clean_notes = notes if notes else "N/A"

        # 4. Create and Save Booking
        current_id = self.next_booking_id
        booking = {
            "booking_id": current_id,
            "name": name,
            "phone": phone,
            "address": address,
            "package": package_info,
            "date": booking_dt.strftime("%Y-%m-%d"),
            "time": booking_dt.strftime("%H:%M"),
            "notes": clean_notes,
            # We don't save 'booked_on' as it complicates the simple text file structure
            "booked_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        }
        
        self.bookings.append(booking)
        self.next_booking_id += 1 # Increment for the next booking
        self.save_bookings()

        print("\n" + "=" * 50)
        print("🎉 BOOKING CONFIRMED!")
        print(f"Booking ID: {booking['booking_id']}")
        print(f"Service: {package_info}")
        print(f"Scheduled For: {booking['date']} at {booking['time']}")
        print("We will contact you shortly!")
        print("=" * 50)


    def view_packages(self):
        """Displays all available packages and their prices."""
        print("\n--- Our Affordable Packages ---")
        
        packages_info = {
            "Basic Wash": ["Exterior hand wash", "Wheel cleaning", "Quick dry"],
            "Premium Wash": ["Everything in Basic", "Interior vacuuming", "Dashboard cleaning", "Air freshener"],
            "Deluxe Detail": ["Everything in Premium", "Complete wax & polish", "Engine bay cleaning", "Carpet shampooing"]
        }
        
        i = 1
        for name, price in self.packages.items():
            print(f"\n[{i}] {name} (₹{price})")
            print("-" * (len(name) + len(str(price)) + 7))
            
            features = packages_info.get(name, [])
            for feature in features:
                print(f"  - {feature}")
            i += 1

    def view_bookings(self):
        """Displays all stored bookings, or allows clearing them."""
        print("\n--- All Bookings ---")
        if not self.bookings:
            print("No bookings found.")
            return

        for booking in self.bookings:
            # Note: We display the booked_on time which is generated at runtime
            # but is not strictly saved/loaded due to the simplified text format
            print("\n" + "=" * 50)
            print(f"ID: {booking['booking_id']} | Date: {booking['date']} at {booking['time']}")
            print(f"Customer: {booking['name']} | Phone: {booking['phone']}")
            print(f"Package: {booking['package']}")
            print(f"Address: {booking['address']}")
            print(f"Notes: {booking['notes']}")
            print("-" * 50)

        # Option to clear bookings
        clear_choice = input("\nDo you want to clear ALL bookings? (y/N): ").lower()
        if clear_choice == 'y':
            self.clear_bookings()

    def clear_bookings(self):
        """Clears all bookings after confirmation."""
        confirm = input("ARE YOU ABSOLUTELY SURE? This cannot be undone. Type 'YES' to confirm: ").strip()
        if confirm == 'YES':
            self.bookings = []
            self.next_booking_id = 1
            self.save_bookings()
            print("✅ All bookings have been successfully cleared.")
        else:
            print("Action cancelled. Bookings were not cleared.")


if __name__ == "__main__":
    app = CarWashCLIApp()
    app.run()