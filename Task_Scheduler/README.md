# Task Scheduler 

## Overview
A Python-based task scheduler designed to manage construction tasks, detect schedule conflicts, and query tasks by supplier. Built with SQLite for data storage and optimized using data structures (hash maps for O(1) lookups, sorting for conflict detection).

## Features
- **Add Tasks**: Store task details (name, start/end dates, supplier ID) in a SQLite database.
- **Conflict Detection**: Identify overlapping tasks using a sorting-based algorithm (O(n log n)).
- **Supplier Queries**: Retrieve tasks by supplier ID with hash map caching for O(1) access.
- **CLI Interface**: User-friendly command-line interface for task management.

## Technologies
- **Python**: Core scripting and logic.
- **SQLite**: Database for task storage and SQL queries (e.g., JOIN, SELECT).
- **Data Structures**: Hash maps for fast lookups, lists for sorting.
- **Libraries**: `sqlite3`, `datetime`, `argparse`.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MicahLarimer/Task-Scheduler.git