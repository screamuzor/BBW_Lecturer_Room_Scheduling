import pandas as pd

def clean_columns (df):
    return df.rename(columns= lambda x : x.strip())

from  data_loader import (
    lecturers,
    courses,
    rooms,
    availability,
    lecturer_courses,
    class_requirements,
    schedule,
    expenses,

)

print ("BBW Lecturer & Room Scheduling Project")
print("Data Validation Starting...")
lecturers = pd.read_csv("../data/lecturers.csv")
print ("\nLecturers dataset loaded successfully!")

print ("\n Datasetshape:")
print(lecturers.shape)
print("\n Column names:")
print(lecturers.columns.tolist())
print ("In Data types:")
print (lecturers.dtypes)

print ("=== BBW DATA VALIDATION ===" )
print("\n1.Missing values")
print("...............")

datasets = {
        "Lecturers": lecturers,
        "Courses": courses,
        "Rooms": rooms,
        "Availability": availability,
        "Lecturer Courses": lecturer_courses,
        "Class Requirements": class_requirements,
        "Schedule": schedule,
        "Expenses": expenses

}

for name, df in datasets.items ():
    missing =df.isnull ().sum().sum()
    print(f"{name}:{missing} missing values")

print("\n2 Duplicate Records")
print(".............")

for name, df in datasets.items ():
    duplicates = df.duplicated().sum()
    print(f"{name}:{duplicates} duplicate rows")

print("\n3. Referential Integrity")
print("...............")

# Check whether every lecturer assigned to the schedule exists in the lecturer dataset

invalid_lecturers = schedule [
    ~schedule["Lecturer_ID"].isin(lecturers["Lecturer_ID"])
]
print(f"Invalid Lecturer IDs in schedule :{len(invalid_lecturers)}")

if len(invalid_lecturers) > 0:
    print(invalid_lecturers[["Schedule_ID", "Lecturer_ID"]])

# schedule to Class Requirement
print("\n Schedule ---> Class Requirements")
print("................")
print("\nClass Requirements columns:")
print(class_requirements.columns.tolist())

invalid_classes = schedule [
    ~schedule["Class_ID"].isin(class_requirements["Class_ID"])
]
print(f"Invalid Class IDs in schedule :{len(invalid_classes)}")
if len(invalid_classes) > 0:
    print(invalid_classes[["Schedule_ID", "Class_ID"]])


# check whether every room assigned to the schedule exists in the rooms dataset

print("\n schedule ------> Rooms")
print("................")
invalid_rooms = schedule [
    ~schedule["Room_ID"].isin(rooms["Room_ID"])

]
print(f"Invalid Room IDs in schedule :{len(invalid_rooms)}")
if len(invalid_rooms) > 0:
    print(invalid_rooms[["Schedule_ID", "Room_ID"]])

# Class Requirements -----> Courses
print("\n class_requirements ------> Course")
print("................")
invalid_courses = class_requirements [
    ~class_requirements["Course_ID"].isin (courses ["Course_ID"])

]
print(f"Invalid Course IDs in class_requirements :{len(invalid_courses)}")
if len(invalid_courses )>0:
    print(invalid_courses[["Class_ID","Course_ID"]])

# Lecturer Courses ____> Lecturers
print("\n Lecturer Courses ---> Lecturers")
print("................")
invalid_lecturers_lc = lecturer_courses [
    ~lecturer_courses[ "Lecturer_ID"].isin(lecturers["Lecturer_ID"])

]
print(f"Invalid Lecturer IDs in lecturer_courses :{len(invalid_lecturers_lc)}")
if len(invalid_lecturers_lc)>0:
    print(invalid_lecturers_lc [["Lecturer_Course_ID", "Lecturer_ID"]])

#Lecture Courses ------> Courses
print("\n Lecture Courses ----> Courses")
print("..........")
invalid_courses_c = courses [
    ~courses["Course_ID"].isin(courses["Course_ID"])

]
print(f"Invalid Course IDs in courses :{len(invalid_courses_c)}")
if len(invalid_courses_c)>0:
    print(invalid_courses_c [["Course_ID", "Course_ID"]])

#Lecture Courses ----> Courses
print ("\n Lecture Courses ----> Courses")
print("....................")
invalid_courses_c = lecturer_courses [
    ~lecturer_courses [ "Course_ID"].isin (courses ["Course_ID"])
]
print(f"Invalid Course IDs in lecturer_courses :{len(invalid_courses_c)}")
if len(invalid_courses_c)>0:
    print(invalid_courses_c [["Lecturer_Course_ID", "Course_ID"]])

# Availability ------> Lecturers
print("\nAvailability ----> Lecturers")
print("....................")

invalid_availability_lecturers = availability[
    ~availability["Lecturer_ID"].isin(lecturers["Lecturer_ID"])
]

print(f"Invalid Lecturer IDs in availability: {len(invalid_availability_lecturers)}")

if len(invalid_availability_lecturers) > 0:
    print(invalid_availability_lecturers[["Availability_ID", "Lecturer_ID"]])

# Expenses --- Lecturers
print("\nExpenses --------->lecturers")
print("....................")
invalid_expense_lecturers = expenses[
       ~expenses ["Lecturer_ID"].isin(lecturers["Lecturer_ID"])
]
print(f"invalid Lecturer IDs in expenses: {len(invalid_expense_lecturers)}")

if len(invalid_expense_lecturers) > 0:
    print(invalid_expense_lecturers [["Expense_ID", "Lecturer_ID" ]])
