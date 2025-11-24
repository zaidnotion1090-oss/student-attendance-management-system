import csv
import datetime
import os

# ================== CONFIG ================== #

FILE = "attendance.csv"
USERNAME = "admin"   # you can change this
PASSWORD = "1234"    # you can change this


# ================= LOGIN SYSTEM ================= #

def login():
    """
    Simple login system for teacher/admin.
    3 attempts allowed.
    """
    print("=========== LOGIN REQUIRED ===========")
    for attempt in range(3):
        user = input("Enter username: ").strip()
        pwd = input("Enter password: ").strip()

        if user == USERNAME and pwd == PASSWORD:
            print("\nLogin successful! Welcome,", user)
            print("======================================\n")
            return True
        else:
            print("Incorrect username or password. Try again.\n")

    print("Too many failed attempts. Exiting program.")
    return False


# ================= FILE HANDLING ================= #

def create_file():
    """
    Creates the attendance.csv file with headers
    if it doesn't already exist.
    """
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Student Name", "Status"])  # header row
        print("attendance.csv created.\n")


def check_file():
    """Ensures the CSV file exists."""
    if not os.path.exists(FILE):
        print("ERROR: attendance.csv not found!")
        return False
    return True


# ================= CORE FUNCTIONS ================= #

def mark_attendance():
    """
    Mark attendance for a student for today's date.
    """
    name = input("Enter student name: ").strip()
    status = input("Present (P) or Absent (A): ").upper().strip()

    if status not in ["P", "A"]:
        print("Invalid status! Please enter P or A only.")
        return

    today = datetime.date.today().strftime("%d-%m-%Y")

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, name, "Present" if status == "P" else "Absent"])

    print(f"Attendance marked for {name} on {today}.")


def view_raw_table():
    """Displays the raw attendance CSV."""
    if not check_file():
        return

    print("\n========== RAW ATTENDANCE TABLE ==========")
    with open(FILE, "r") as f:
        for row in csv.reader(f):
            print(row)
    print("==========================================\n")


def view_attendance():
    """View complete raw CSV attendance table"""
    view_raw_table()


# ================= ATTENDANCE FREQUENCY ================= #

def calculate_frequency():
    """
    Returns attendance summary in the format:
    {
        "aaryan": {"present": x, "absent": y},
        "rohan": {"present": x, "absent": y},
    }
    """
    freq = {}

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row

        for date, name, status in reader:
            name_key = name.strip().lower()

            if name_key not in freq:
                freq[name_key] = {"present": 0, "absent": 0}

            if status == "Present":
                freq[name_key]["present"] += 1
            else:
                freq[name_key]["absent"] += 1

    return freq


# ================= REPORT FUNCTIONS ================= #

def full_summary_report():
    """Shows summary of all students."""
    if not check_file():
        return

    freq = calculate_frequency()

    print("\n========== FULL SUMMARY REPORT ==========")
    print("Name\t\tPresent\tAbsent\tPercentage")
    print("----------------------------------------")

    for name, data in freq.items():
        total = data["present"] + data["absent"]
        percent = (data["present"] / total * 100) if total > 0 else 0
        print(f"{name.title():<15}{data['present']}\t{data['absent']}\t{percent:.2f}%")

    print("========================================\n")


def view_full_report():
    full_summary_report()


def individual_report():
    """Shows report for a single student."""
    if not check_file():
        return

    student = input("Enter student name: ").strip().lower()
    freq = calculate_frequency()

    if student not in freq:
        print("No records found for", student.title())
        return

    data = freq[student]
    total = data["present"] + data["absent"]
    percent = (data["present"] / total * 100) if total > 0 else 0

    print("\n========== STUDENT REPORT ==========")
    print("Name       :", student.title())
    print("Total Days :", total)
    print("Present    :", data["present"])
    print("Absent     :", data["absent"])
    print("Attendance :", f"{percent:.2f}%")
    print("====================================\n")


def student_report():
    individual_report()


def monthly_report():
    """Shows month-wise report for a student."""
    if not check_file():
        return

    student = input("Enter student name: ").strip().lower()
    monthly = {}

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)

        for date, name, status in reader:
            if name.strip().lower() != student:
                continue

            day, month, year = date.split("-")
            month = int(month)

            if month not in monthly:
                monthly[month] = {"present": 0, "absent": 0}

            if status == "Present":
                monthly[month]["present"] += 1
            else:
                monthly[month]["absent"] += 1

    if not monthly:
        print("No records available for", student.title())
        return

    print("\n====== MONTHLY REPORT ======")
    for month, data in monthly.items():
        total = data["present"] + data["absent"]
        percent = (data['present'] / total * 100) if total else 0
        print(f"Month {month:02d}: Present={data['present']}, Absent={data['absent']}, Percentage={percent:.2f}%")
    print("=============================\n")


# ================= MENU ================= #

def menu():
    create_file()

    if not login():
        return

    while True:
        print("=========== ATTENDANCE SYSTEM ===========")
        print("1. Mark Attendance")
        print("2. View Raw Attendance Table")
        print("3. View Full Summary Report")
        print("4. View Individual Student Report")
        print("5. View Monthly Report for a Student")
        print("6. Exit")
        print("=========================================")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_raw_table()
        elif choice == "3":
            full_summary_report()
        elif choice == "4":
            individual_report()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")


# ================= MAIN ENTRY ================= #

if __name__ == "__main__":
    menu()
