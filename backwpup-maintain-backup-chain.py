#!/usr/bin/env python3

import datetime
import os
import glob
import sys

def generate_date_matrix(year):
    date_matrix = []
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(days=1)
    
    current_date = start_date
    while current_date <= end_date:
        date_matrix.append(current_date.strftime("%Y-%m-%d"))
        current_date += delta
    
    return date_matrix

def filter_dates(date_matrix):
    filtered_dates = []
    for date in date_matrix:
        day = int(date.split('-')[2])
        if day not in [1, 15, 28]:
            filtered_dates.append(date)
    return filtered_dates

def delete_files_for_dates(directory, dates):
    for date in dates:
        pattern = os.path.join(directory, f"{date}_*.zip")
        matched_files = glob.glob(pattern)
        for file in matched_files:
            os.remove(file)
            print(f"Deleted: {file}")

def main(directory):
    current_year = datetime.datetime.now().year
    date_matrix = generate_date_matrix(current_year)
    
    filtered_dates = filter_dates(date_matrix)
    
    # Get the current date
    now = datetime.datetime.now()
    
    # Calculate the start of the last month
    first_day_of_current_month = now.replace(day=1)
    last_month = first_day_of_current_month - datetime.timedelta(days=1)
    start_date = datetime.date(current_year, 1, 1)
    end_date = datetime.date(last_month.year, last_month.month, last_month.day)

    # Collect dates from the end of the last month backwards to January 1st
    dates_to_check = []
    for date in reversed(filtered_dates):
        current_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if start_date <= current_date <= end_date:
            dates_to_check.append(date)
    
    # Delete matching files
    delete_files_for_dates(directory, dates_to_check)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./date_matrix.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    main(directory)
