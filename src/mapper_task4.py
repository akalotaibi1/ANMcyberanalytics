#!/usr/bin/env python3
# Task 4: The Time Dimension
# Research Question: How has the total number of crimes changed over the years?
# Column: Date at index 2 (0-based), format: MM/DD/YYYY HH:MM:SS AM/PM
import sys

DATE_IDX = 2

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    parts = line.split(',')

    if len(parts) <= DATE_IDX:
        continue

    # Skip header row
    if parts[0] == 'ID':
        continue

    date_str = parts[DATE_IDX].strip()

    if date_str:
        # Parse year: "01/10/2024 02:30:00 PM" -> split by space -> "01/10/2024" -> split by / -> "2024"
        try:
            date_part = date_str.split(' ')[0]   # "01/10/2024"
            year = date_part.split('/')[2]        # "2024"
            print(f"{year}\t1")
        except IndexError:
            continue
