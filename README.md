# 🏫 BBW Institutional Resource & Scheduling Engine

A data pipeline and constraint-matching validation engine built to support academic scheduling, room allocations, and lecturer availability verification at bbw Hochschule.

---

##  Project Architecture & Components

The system is organized into a modular structure separating the relational data layer, structural validations, and core scheduling logic:

```text
BBW_Lecturer_Room_Scheduling/
│
├── data/                  # Cleaned operational CSV datasets
│   ├── availability.csv
│   ├── class_requirements.csv
│   ├── courses.csv
│   ├── rooms.csv
│   └── schedule.csv
│
├── src/                   # Source scripts & processing core
│   ├── data_loader.py     # Resilient hybrid ingestion script (SQL/CSV fallback)
│   ├── data_validation.py # Data integrity and quality assurance checks
│   ├── database.py        # PostgreSQL schema initialization and management
│   └── scheduler.py       # Core constraint-matching allocation engine
│
├── .gitignore             # Explicitly excludes temporary pycache data
└── README.md              # Project documentation
```

---

##  Core Operational Workflows

### 1. Resilient Data Layer (`src/data_loader.py` & `src/database.py`)
- **Dual-Engine Ingestion:** Integrates a hybrid data framework using `SQLAlchemy` and `psycopg2`. 
- **Graceful Fallback:** Automates fallback processing. If a local production PostgreSQL database instance is unreachable, the system automatically routes tasks to read from localized `.csv` files inside the `data/` folder.

### 2. Quality Assurance (`src/data_validation.py`)
- Standardizes inconsistent dataset inputs across raw tables (e.g., matching varying naming conventions like `Employment_Type` to strict internal system standards).
- Strips trailing whitespaces and neutralizes `NaN` missing values across rows before pushing records downstream.

### 3. Constraint-Matching Engine (`src/scheduler.py`)
- **Room & Equipment Matching:** Parses incoming class data requests and dynamically isolates physical spaces that satisfy both room layouts and specialized equipment needs.
- **Availability Matrix Validation:** Cross-references open slots against declared shifts, filtering out lecturers who are not set to `Available` on a given calendar horizon.
- **Overlap Prevention (`is_lecturer_free`):** Evaluates pre-existing active class calendars to eliminate time-slot over-allocations for rooms and lecturers simultaneously.

---

##  Quick Start Guide

### Prerequisites
Ensure you have Python 3.10+ and a package manager installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/screamuzor/BBW_Lecturer_Room_Scheduling.git
cd BBW_Lecturer_Room_Scheduling
   ```

2. **Install dependencies:**
  pip install -r requirements.txt
   ```

3. **Run the scheduling engine:**
     
python src/scheduler.py
The system loads the project datasets, validates scheduling constraints, checks lecturer availability and qualifications, matches suitable rooms, and reports successful allocations or scheduling conflicts.

---

##  Business Impact & Value
Traditional university resource scheduling is frequently prone to manual data collisions and space misallocations. This automated prototype transforms raw tabular records into a structured programmatic framework, shifting operational planning from reactive troubleshooting to proactive automation.
