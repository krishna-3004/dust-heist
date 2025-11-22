# Project Statement – Dust Heist

## Problem Statement
Small and medium car wash businesses often handle bookings manually using phone calls, paper notes, or simple spreadsheets, which leads to errors, data loss, and difficulty tracking customer appointments. There is a need for a lightweight system that standardizes bookings, reduces manual effort, and works without complex infrastructure.

## Scope of the Project
This project focuses on a single-application, command-line booking system that:
- Manages doorstep car wash bookings.
- Stores booking data in a structured, file-based format on a single machine.
- Supports basic operations: create booking, view packages, list bookings, and clear all bookings.
- Does not include payments, multi-user access control, or a graphical/web interface in this version.

## Target Users
- Individual car wash business owners and small teams.
- Operators who need a simple tool to record and look up bookings.
- Students and developers learning about CLI apps, file I/O, and basic software design.

## High-level Features
- CLI-based main menu to navigate all core actions.
- Predefined car wash packages (Basic, Premium, Deluxe) with fixed pricing.
- Booking flow with validation for customer details, phone, and future date/time.
- Auto-generated booking IDs for unique identification.
- Persistent file storage (`car_wash_bookings.txt`) using custom record and field delimiters.
- Ability to list all saved bookings and to clear all bookings with confirmation.
