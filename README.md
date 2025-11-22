# dust-heist
# Dust Heist – Doorstep Car Wash Booking System

## Project Title
Dust Heist – Doorstep Car Wash Booking System

## Overview of the Project
Dust Heist is a Python-based command-line application that allows customers to book doorstep car wash services, choose from multiple wash packages, and store booking details persistently in a local text file using custom delimiters. It is designed for small car wash businesses that need a simple, offline-friendly booking management tool without a full database setup.

## Features
- Interactive CLI menu (book service, view packages, list bookings, clear bookings, exit).
- Three predefined car wash packages: Basic Wash, Premium Wash, Deluxe Detail with fixed prices.
- Booking creation with validation for name, 10-digit phone number, address, package selection, and future date/time.
- Auto-incrementing booking ID maintained across runs.
- Persistent storage of all bookings in `car_wash_bookings.txt` using record and field delimiters.
- View all bookings in a formatted output.
- Option to clear all bookings with confirmation and reset of booking IDs.

## Technologies / Tools Used
- Python 3
- Python standard library modules: `os`, `datetime`, `re`
- File-based storage using `car_wash_bookings.txt`
- Command-line interface (terminal)

## Steps to Install & Run the Project

1. **Clone the repository**

