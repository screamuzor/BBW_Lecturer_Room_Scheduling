import psycopg2

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:uzomaeze007@localhost:5432/bbw_scheduler"
)

tables = {
    "lecturers": "../data/lecturers.csv",
    "courses": "../data/courses.csv",
    "rooms": "../data/rooms.csv",
    "availability": "../data/availability.csv",
    "lecturer_courses": "../data/lecturer_courses.csv",
    "class_requirements": "../data/class_requirements.csv",
    "schedule": "../data/schedule.csv",
    "expenses": "../data/expenses.csv"

}

column_mapping = {
    "lecturers": {
        "Employment_Type": "Employment_Status",
        "Specialisation": "Specialization",
        "Hourly_Rate_EUR": "Hourly_Rate",
        "Preferred_Time": "Preferred_Shift"
    },
    "courses": {
        "Required_Equipment": "Equipment"
    },

}

for table_name, file_path in tables.items():

    data = pd.read_csv(file_path)

    if table_name in column_mapping:
        data = data.rename(columns=column_mapping[table_name])
    data.columns = data.columns.str.lower()
    data.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"{table_name}: {len(data)} rows loaded")

print("All data loaded successfully into PostgreSQL.")

connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="bbw_scheduler",
    user="postgres",
    password="uzomaeze007"
)

print("PostgreSQL connection successful!")

connection.close()