import sqlite3

# ==============================
# DATABASE SETUP
# ==============================
def setup_database():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        po_number TEXT,
        approved_hours INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        project_id INTEGER,
        assigned_to TEXT,
        estimated_hours INTEGER,
        billing_hours INTEGER,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    conn.commit()
    conn.close()

# ==============================
# FEATURE 1: Create New Project
# ==============================
def create_project():
    name = input("Enter project name: ")
    po_number = input("Enter PO number: ")
    approved_hours = input("Enter approved hours: ")
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (name, po_number, approved_hours) VALUES (?, ?, ?)", (name, po_number, approved_hours))
    conn.commit()
    conn.close()
    print("Project added successfully.\n")

# ==============================
# FEATURE 2: Add Task to Project
# ==============================
def add_task():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM projects")
    projects = cursor.fetchall()
    if not projects:
        print("No projects found.\n")
        return
    print("Available Projects:")
    for p in projects:
        print(f"{p[0]}: {p[1]}")
    project_id = input("Enter Project ID: ")
    title = input("Task title: ")
    description = input("Description: ")
    assigned_to = input("Assigned to: ")
    estimated = input("Estimated hours: ")
    billed = input("Billing hours: ")
    status = input("Status: ")
    cursor.execute('''
    INSERT INTO tasks (title, description, project_id, assigned_to, estimated_hours, billing_hours, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, project_id, assigned_to, estimated, billed, status))
    conn.commit()
    conn.close()
    print("Task added.\n")

# ==============================
# FEATURE 3: View Project Dashboard
# ==============================
def view_dashboard():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM projects")
    projects = cursor.fetchall()
    for project in projects:
        print(f"\nProject: {project[1]} (ID: {project[0]})")
        cursor.execute("SELECT title, assigned_to, status, estimated_hours, billing_hours FROM tasks WHERE project_id = ?", (project[0],))
        tasks = cursor.fetchall()
        for task in tasks:
            title, assigned, status, est, bill = task
            burnout = f"{round(int(bill)/int(est)*100)}%" if int(est) > 0 else "N/A"
            print(f"  Task: {title}, Assigned: {assigned}, Status: {status}, Estimated: {est}, Billed: {bill}, Burnout: {burnout}")
    conn.close()

# ==============================
# FEATURE 4: Update Task Info
# ==============================
def update_task():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks found.\n")
        return
    for t in tasks:
        print(f"{t[0]}: {t[1]}")
    task_id = input("Enter Task ID: ")
    print("1. Title\n2. Assigned To\n3. Status\n4. Estimated Hours\n5. Billing Hours")
    choice = input("Choose field to update: ")
    field_map = {'1': 'title', '2': 'assigned_to', '3': 'status', '4': 'estimated_hours', '5': 'billing_hours'}
    if choice not in field_map:
        print("Invalid choice.")
        return
    new_val = input("New value: ")
    cursor.execute(f"UPDATE tasks SET {field_map[choice]} = ? WHERE id = ?", (new_val, task_id))
    conn.commit()
    conn.close()
    print("Task updated.\n")

# ==============================
# FEATURE 5: Delete Task or Project
# ==============================
def delete_task_or_project():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    print("1. Delete Task\n2. Delete Project (and its tasks)")
    choice = input("Enter your choice: ")
    if choice == '1':
        cursor.execute("SELECT id, title FROM tasks")
        tasks = cursor.fetchall()
        for t in tasks:
            print(f"{t[0]}: {t[1]}")
        task_id = input("Enter Task ID: ")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            print("Task deleted.\n")
    elif choice == '2':
        cursor.execute("SELECT id, name FROM projects")
        projects = cursor.fetchall()
        for p in projects:
            print(f"{p[0]}: {p[1]}")
        project_id = input("Enter Project ID: ")
        confirm = input("Are you sure? This will delete all tasks in it too. (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("DELETE FROM tasks WHERE project_id = ?", (project_id,))
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            print("Project and tasks deleted.\n")
    else:
        print("Invalid option.")
    conn.close()

# ==============================
# MAIN MENU
# ==============================
def main():
    while True:
        print("\n==== ENGINEERING TASK TRACKER ====")
        print("1. Create New Project")
        print("2. Add Task to Project")
        print("3. View Project Dashboard")
        print("4. Update Task Information")
        print("5. Delete Task or Project")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            create_project()
        elif choice == '2':
            add_task()
        elif choice == '3':
            view_dashboard()
        elif choice == '4':
            update_task()
        elif choice == '5':
            delete_task_or_project()
        elif choice == '6':
            print("Goodbye.")
            break
        else:
            print("Invalid choice.\n")

# ==============================
# ENTRY POINT
# ==============================
setup_database()
main()