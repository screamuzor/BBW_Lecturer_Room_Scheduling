import pandas as pd

generated_schedule = []

# Import all project datasets from the data loader
from data_loader import (
    lecturers,
    courses,
    rooms,
    availability,
    lecturer_courses,
    class_requirements,
    schedule,
    expenses
)
# ============================================================
# BBW LECTURER & ROOM SCHEDULING SYSTEM
# Scheduling Engine
# ============================================================
print("BBW Lecturer & Room Scheduling Systems")
print("Scheduling Engine Starting..")


# ============================================================
# FIND SUITABLE ROOMS FOR A CLASS
# ============================================================
def find_suitable_rooms (class_id):
    # Find the requirements for the selected class
    class_info = class_requirements [
        class_requirements ["Class_ID"] == class_id
    ]

    # Return an empty DataFrame if the class does not exist
    if class_info.empty:
         return pd.DataFrame()

    # Get the room requirements for the class
    required_room_type = class_info.iloc[0] ["Required_Room_Type"]
    required_equipment = class_info.iloc[0] ["Required_Equipment"]

    # Clean the required room type
    required_room_type = " ".join(
        str(required_room_type).split()
    )

    # Clean room type data
    room_type_clean = rooms["Room_Type"].fillna("").apply(
        lambda x: " ".join(str(x).split())
    )

    # Find rooms that satisfy the requirements
    suitable_rooms = rooms[
        (room_type_clean == required_room_type) &
        (rooms["Equipment"].fillna("").str.contains(
            str(required_equipment),
            na=False
        ))
    ]

    return suitable_rooms

# ============================================================
# TEST ROOM SELECTION
# ============================================================

print("\n Suitable rooms for CL001:")
print(find_suitable_rooms("CL001"))

# Add the selected room to the schedule
print("\nRoom Types:")
print (rooms["Room_Type"].unique())
print("\n Equipment:")
print(rooms["Equipment"].unique())
print("nCL001 requirements:")
print(class_requirements [
    class_requirements ["Class_ID"] == "CL001"
][["Required_Room_Type", "Required_Equipment"]])


# ============================================================
# FIND QUALIFIED LECTURERS FOR A CLASS
# ============================================================

def find_qualified_lecturers (class_id):
    # Find the course assigned to the selected class
    class_info= class_requirements [
        class_requirements["Class_ID"] == class_id
    ]

    # Return an empty DataFrame if the class does not exist
    if class_info.empty:
            return pd.DataFrame()

    course_id = class_info.iloc[0] ["Course_ID"]

    # Find Lecturers qualified to teach the course
    qualified_lecturers = lecturer_courses[
        (lecturer_courses["Course_ID"] == course_id) &
        (lecturer_courses["Primary_Assignment"] =="Yes")
    ]
    # Match the qualified lecturers with the lecturer dataset
    qualified_lecturers = qualified_lecturers.merge(
        lecturers,
        on= "Lecturer_ID",
        how = "inner"
    )
    return qualified_lecturers

# ============================================================
# TEST QUALIFIED LECTURER SELECTION
# ============================================================

print("\n Qualified lecturers for CL001:")
print(find_qualified_lecturers("CL001"))


# ============================================================
# CHECK LECTURER AVAILABILITY
# ============================================================
def check_lecturer_availability(lecturer_id, day, time_slot):

    lecturer_availability = availability[
        availability["Lecturer_ID"].astype(str).str.strip().eq(str(lecturer_id).strip()) &
        availability["Day"].astype(str).str.strip().eq(str(day).strip()) &
        availability["Time_Slot"].astype(str).str.strip().eq(str(time_slot).strip())
    ]

    if lecturer_availability.empty:
        return False

    return str(lecturer_availability.iloc[0]["Availability_Status"]).strip() == "Available"

# ============================================================
# CHECK ROOM AVAILABILITY
# ============================================================
def check_room_availability(room_id, day, time_slot):
    existing_schedule = schedule[
        (schedule["Room_ID"] == room_id) &
        (schedule["Day"] == day) &
        (schedule["Time_Slot"] == time_slot)
    ]

    generated_bookings = [
        booking for booking in generated_schedule
        if booking["Room_ID"] == room_id
        and booking["Day"] == day
        and booking["Time_Slot"] == time_slot
    ]

    return existing_schedule.empty and len(generated_bookings) == 0

# ============================================================
# TEST ROOM AVAILABILITY
# ============================================================
print("\nIs Room R001 free on Monday at 08:00-10:00?:")
print(check_room_availability("R001", "Monday", "08:00-10:00"))

# ============================================================
# TEST LECTURER AVAILABILITY
# ============================================================
print("\n Is Lecturer L001 available on Monday at 14:00-16:00?:")
print(check_lecturer_availability("L001", "Monday", "14:00-16:00"))

# ============================================================
# CHECK IF LECTURER IS ACTUALLY FREE
# ============================================================
def is_lecturer_free (lecturer_id,day,time_slot):
    # First check declared availability
    declared_available = check_lecturer_availability (
        lecturer_id,
        day,
        time_slot
    )
# check whether the lecturer is already teaching
#another class at the same time
    already_booked = schedule[
        (schedule["Lecturer_ID"] == lecturer_id) &
        (schedule["Day"] == day) &
        (schedule["Time_Slot"] == time_slot)

    ]
# Lecturer must be declared available AND , must not already be booked
    return declared_available and already_booked.empty



# ============================================================
# ASSIGN CLASS TO ROOM AND LECTURER
# ============================================================
def assign_class(class_id, day, time_slot):
    # 1. Find suitable rooms for this class
    suitable_rooms = find_suitable_rooms(class_id)
    if suitable_rooms.empty:
        return {
            "Status": "Failed",
            "Message": f"No suitable rooms found for class {class_id}."
        }

    # 2. Find a room among the suitable ones that is actually free
    selected_room_id = None
    for room_id in suitable_rooms["Room_ID"]:
        # UPDATED: Changed from is_room_free to your function check_room_availability
        if check_room_availability(room_id, day, time_slot):
            selected_room_id = room_id
            break

    if not selected_room_id:
        return {
            "Status": "Failed",
            "Message": f"No free suitable rooms available on {day} at {time_slot}."
        }

    # 3. Find the Course_ID for this class
    class_info = class_requirements[class_requirements["Class_ID"] == class_id]
    if class_info.empty:
        return {
            "Status": "Failed",
            "Message": f"Class {class_id} not found."
        }
    course_id = class_info.iloc[0]["Course_ID"]

    # 4. Find qualified lecturers for this course using your find_qualified_lecturers logic
    qualified_lecturers = find_qualified_lecturers(class_id)
    if qualified_lecturers.empty:
        return {
            "Status": "Failed",
            "Message": f"No qualified lecturers assigned to class {class_id}."
        }

    # 5. Find an available lecturer
    selected_lecturer_id = None
    for l_id in qualified_lecturers["Lecturer_ID"]:
        # UPDATED: Changed from is_lecturer_available to your function check_lecturer_availability
        if is_lecturer_free(l_id, day, time_slot):
            selected_lecturer_id = l_id
            break

    if not selected_lecturer_id:
        return {
            "Status": "Failed",
            "Message": f"No qualified and available lecturers on {day} at {time_slot}."
        }
    print("Qualified lecturers:")
    print(qualified_lecturers[["Lecturer_ID", "Lecturer_Name"]])

    # 6. Return assignment details
    return {
        "Status": "Success",
        "Class_ID": class_id,
        "Room_ID": selected_room_id,
        "Lecturer_ID": selected_lecturer_id,
        "Day": day,
        "Time_Slot": time_slot
    }

print("\nAssignment for CL002:")
print(assign_class("CL002", "Tuesday", "18:00-20:00"))
print("\nCL002 qualified lecturers:")
print(find_qualified_lecturers("CL002")[[
    "Lecturer_ID",
    "Lecturer_Name",
    "Primary_Assignment",
    "Status"
]])

# ============================================================
# GENERATE A SCHEDULE FOR ALL CLASSES
# ============================================================
def generate_schedule():
    print("\nGenerating schedule...")
    days=[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    time_slots = [
        "08:00-10:00",
        "10:00-12:00",
        "12:00-14:00",
        "14:00-16:00",
        "16:00-18:00",
        "18:00-20:00",
    ]

    for class_id in class_requirements["Class_ID"]:
        print("\nScheduling:", class_id)

        # New Schedule placed as false
        scheduled = False

        for day in days:
            for time_slot in time_slots:
                assignment = assign_class(class_id, day, time_slot)

                if assignment["Status"] == "Success":
                    print("Success:", assignment)
                    generated_schedule.append(assignment)
                    scheduled = True
                    break

            if scheduled:
                break

        if not scheduled:
            print("Failed:", class_id)

    return generated_schedule

generated_schedule = generate_schedule()

print("\nGenerated Schedule:")
print(generated_schedule)
