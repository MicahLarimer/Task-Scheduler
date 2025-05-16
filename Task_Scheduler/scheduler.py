import sqlite3
from datetime import datetime
import argparse

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            supplier_id INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

# Convert date string (YYYY-MM-DD) to datetime for comparison
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")

# Add a task to the database
def add_task(cursor, conn, task_name, start_date, end_date, supplier_id):
    cursor.execute(
        "INSERT INTO tasks (task_name, start_date, end_date, supplier_id) VALUES (?, ?, ?, ?)",
        (task_name, start_date, end_date, supplier_id)
    )
    conn.commit()
    print(f"Added task: {task_name}")

# Check for schedule conflicts using sorting (O(n log n))
def check_conflicts(cursor):
    cursor.execute("SELECT task_id, task_name, start_date, end_date FROM tasks")
    tasks = cursor.fetchall()
    # Convert to list of tuples with datetime objects
    task_list = [
        (t[0], t[1], parse_date(t[2]), parse_date(t[3]))
        for t in tasks
    ]
    # Sort by start date
    task_list.sort(key=lambda x: x[2])
    conflicts = []
    # Check for overlaps
    for i in range(1, len(task_list)):
        prev_task = task_list[i-1]
        curr_task = task_list[i]
        if curr_task[2] < prev_task[3]:  # Current task starts before previous ends
            conflicts.append((prev_task[1], curr_task[1]))
    return conflicts

# Query tasks by supplier using hash map for O(1) lookup
def get_tasks_by_supplier(cursor, supplier_id):
    cursor.execute("SELECT task_name, start_date, end_date FROM tasks WHERE supplier_id = ?", (supplier_id,))
    tasks = cursor.fetchall()
    # Cache results in a dictionary for quick access
    task_dict = {t[0]: {"start": t[1], "end": t[2]} for t in tasks}
    return task_dict

# Main CLI function
def main():
    parser = argparse.ArgumentParser(description="Construction Task Scheduler")
    parser.add_argument("--add", action="store_true", help="Add a new task")
    parser.add_argument("--name", type=str, help="Task name")
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--supplier", type=int, help="Supplier ID")
    parser.add_argument("--check-conflicts", action="store_true", help="Check for schedule conflicts")
    parser.add_argument("--get-supplier", type=int, help="Get tasks for a supplier ID")
    
    args = parser.parse_args()
    
    conn, cursor = init_db()
    
    try:
        if args.add and all([args.name, args.start, args.end, args.supplier]):
            # Validate dates
            start_date = parse_date(args.start)
            end_date = parse_date(args.end)
            if end_date <= start_date:
                raise ValueError("End date must be after start date")
            add_task(cursor, conn, args.name, args.start, args.end, args.supplier)
        
        if args.check_conflicts:
            conflicts = check_conflicts(cursor)
            if conflicts:
                print("Schedule conflicts found:")
                for t1, t2 in conflicts:
                    print(f"- {t1} overlaps with {t2}")
            else:
                print("No schedule conflicts found")
        
        if args.get_supplier is not None:
            tasks = get_tasks_by_supplier(cursor, args.get_supplier)
            if tasks:
                print(f"Tasks for Supplier {args.get_supplier}:")
                for name, details in tasks.items():
                    print(f"- {name}: {details['start']} to {details['end']}")
            else:
                print(f"No tasks found for Supplier {args.get_supplier}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()