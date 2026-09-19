import pandas as pd
lecturers = pd.read_csv ("../data/lecturers.csv")
courses = pd.read_csv ("../data/courses.csv")
rooms = pd.read_csv("../data/rooms.csv")
availability = pd.read_csv ("../data/availability.csv")
lecturer_courses = pd.read_csv ("../data/lecturer_courses.csv")
class_requirements = pd.read_csv ("../data/class_requirements.csv")
schedule = pd.read_csv ("../data/schedule.csv")
expenses = pd.read_csv ("../data/expenses.csv")

print( "All datasets loaded successfully")
print("\n Lecturers")
print(lecturers.head())

print("\n Courses")
print(courses.head ())


print("\n Rooms")
print(rooms.head())

print ("\n Availability")
print(availability.head())

print ('\n Lecturer Courses')
print(lecturer_courses.head())

print("\n class_requirements")
print(class_requirements.head())

print("\n Schedule")
print(schedule.head())

print("\n Expenses")
print(expenses.head())

print("\n Lecturer dataset size:")
print(lecturers.shape)

print("\n Courses")
print(courses.shape)

print("\n Dataset Summary")

print ("Lecturers", lecturers.shape)
print ("Courses", courses.shape)
print ("Rooms", rooms.shape)
print("Availability", availability.shape)
print("Lecturer Courses", lecturer_courses.shape)
print("Class Requirements:", class_requirements.shape)
print("Schedule:", schedule.shape)
print("Expenses:", expenses.shape)

print("\nCourses",)
print(courses.columns)

print("\nMissing values:")
print(lecturers.isnull().sum())