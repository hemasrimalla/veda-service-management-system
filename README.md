# Veda Technology Business & Service Management System

A beginner-friendly, modular, menu-driven Python command-line application simulating the day-to-day operations of **Veda Technology**—a digital solutions consulting firm and technology training academy.

The system manages commercial IT services, educational and internship programs, customer accounts, and client inquiries with full CRUD functionality, multi-criteria filtering, executive reporting, and error-resilient JSON persistence.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Project Structure](#project-structure)
4. [Python Concepts Applied](#python-concepts-applied)
5. [Prerequisites & Installation](#prerequisites--installation)
6. [How to Run the Application](#how-to-run-the-application)
7. [Running the Automated Tests](#running-the-automated-tests)
8. [Menu Walkthrough & Sample Output](#menu-walkthrough--sample-output)
9. [Data Storage & Sample Records](#data-storage--sample-records)
10. [Future Improvements](#future-improvements)
11. [Git Setup & Push Instructions](#git-setup--push-instructions)

---

## Project Overview

Organizations like Veda Technology provide dual-track offerings:
1. **Digital IT Services**: Enterprise Web Development, Cloud Consulting & DevOps, Mobile App Development, AI/ML Integrations, and Data Analytics.
2. **Academy Programs**: Professional bootcamps, hands-on internships, and corporate technology upskilling cohorts.

This application acts as a unified terminal ERP platform to track offerings, maintain client relationships, handle incoming inquiries with priority and status tracking, calculate cohort capacity and revenue projections, and export operational reports to plain text and CSV.

---

## Key Features

1. **Digital Service Management (`modules/service_manager.py`)**:
   - Add, view, update, and delete service offerings.
   - Fields: `id`, `name`, `category`, `description`, `price`, `status` (`Active` / `Inactive`).
   - Clean tabular formatting with automated column truncation.

2. **Program & Internship Management (`modules/program_manager.py`)**:
   - Add, view, update, and delete training programs and sponsored internships.
   - Fields: `id`, `name`, `type` (`Training`, `Internship`, `Technology`), `duration`, `fee`, `seats`, `start_date` (`YYYY-MM-DD`), `status`.

3. **Customer & Inquiry Management (`modules/inquiry_manager.py`)**:
   - Register clients and individual students (`id`, `name`, `email`, `phone`, `company`, `registered_date`).
   - Log customer inquiries linked directly to a client and a target service or program.
   - Track lifecycle status (`Open`, `In Progress`, `Resolved`, `Closed`) and priority tier (`Low`, `Medium`, `High`, `Urgent`).

4. **Multi-Criteria Search & Filtering (`modules/search_filter.py`)**:
   - Keyword search across service titles, program titles, categories, and descriptions.
   - Filter services by category, status, and price range (`$ Min` – `$ Max`).
   - Filter programs by track type, status, and fee range.
   - Filter inquiries by status, priority tier, or customer.

5. **Business Analytics & Reporting (`modules/reports.py`)**:
   - **Executive Summary**: Catalog counts, active vs. inactive service distribution, open inquiry pipeline.
   - **Inquiry Status & Priority Distribution**: Percentage breakdowns across stages.
   - **Demand Ranking**: Identifying top-requested services and popular training cohorts.
   - **Capacity & Revenue Projection**: Total available seats, average tuition, and potential revenue calculation (`seats * fee`).
   - **Exporting**: Export comprehensive executive reports to formatted Plain Text (`.txt`) or multi-table CSV (`.csv`).

6. **Error-Resilient JSON Persistence (`modules/storage.py`)**:
   - Auto-creates `data/` folder and files on first launch.
   - Pre-seeded with realistic, synthetic sample data (at least 6 records per entity).
   - Graceful recovery: handles empty or corrupted JSON files with clear user warnings without crashing.

---

## Project Structure

```text
veda-business-management-system/
├── main.py                     # Menu-driven CLI entry point
├── models/
│   ├── __init__.py             # Exposes domain classes
│   ├── service.py              # Service model (attributes, to_dict, from_dict)
│   ├── program.py              # Program model (training/internship/tech cohorts)
│   ├── customer.py             # Customer entity (client & student registry)
│   └── inquiry.py              # Inquiry model (linked to customer & target offering)
├── modules/
│   ├── __init__.py             # Module package marker
│   ├── service_manager.py      # CRUD operations & views for digital services
│   ├── program_manager.py      # CRUD operations & views for programs/internships
│   ├── inquiry_manager.py      # Customer registration & inquiry lifecycle
│   ├── search_filter.py        # Multi-attribute search and filtering engine
│   ├── reports.py              # Business analytics, aggregations & file exports
│   ├── storage.py              # JSON load/save helpers & corrupted file handling
│   └── validators.py           # Input validation loops, dates, positive numbers
├── data/
│   ├── services.json           # Seeded services dataset
│   ├── programs.json           # Seeded programs dataset
│   ├── customers.json          # Seeded customer registry
│   └── inquiries.json          # Seeded customer inquiries
├── sample_output/
│   ├── sample_run.txt          # Complete recorded execution transcript
│   ├── veda_executive_report.txt # Exported plain text business report
│   └── veda_business_metrics.csv # Exported structured CSV metrics
├── test_system.py              # Automated unittest suite (11 tests)
├── generate_sample_run.py      # Interactive automation script
├── README.md                   # Comprehensive documentation
└── .gitignore                  # Git ignore rules for Python bytecode and OS files
```

---

## Python Concepts Applied

- **Classes & Object-Oriented Programming (OOP)**:
  - Custom classes (`Service`, `Program`, `Customer`, `Inquiry`) encapsulate state and behaviors.
  - Serialization methods `to_dict()` and class factory deserializers `from_dict(data)`.
  - Magic methods `__str__()` for user-friendly string formatting.
- **Modules & Packages**:
  - Logical separation of concerns across `models/` and `modules/` folders with clean `__init__.py` packaging.
- **File I/O & Exception Handling**:
  - Reading and writing UTF-8 encoded JSON and CSV files.
  - Protecting against `json.JSONDecodeError`, `FileNotFoundError`, `OSError`, and `ValueError`.
- **Input Validation & Defensive Programming**:
  - Interactive retry loops verifying non-empty strings, positive floats/integers, date formats (`YYYY-MM-DD`), choice sets, and unique primary keys.
- **Data Structures**:
  - Dictionaries and lists for in-memory collections and aggregations.
  - Python's standard `collections.Counter` for demand ranking and status frequency counting.

---

## Prerequisites & Installation

- **Python Version**: Python 3.8 or higher (No third-party libraries required; uses Python Standard Library only).
- **Git**: Installed for version control.

### Clone the Repository:
```bash
git clone https://github.com/hemasrimalla/veda-business-management-system.git
cd veda-business-management-system
```

---

## How to Run the Application

Launch the application directly with Python:
```bash
python main.py
```

### Main Navigation Menu:
```text
====================================================
                MAIN NAVIGATION MENU                
====================================================
  1. Digital Service Management
  2. Program & Internship Management
  3. Customer & Inquiry Management
  4. Search & Multi-Criteria Filtering
  5. Business Analytics & Reports
  6. System Data Status & Reload
  7. Exit Application
====================================================
Select an option (1-7):
```

---

## Running the Automated Tests

An automated test suite is included in `test_system.py`, validating serialization, CRUD, storage resilience, input validators, and reporting logic without requiring user typing:

```bash
python test_system.py
```

**Test Output:**
```text
Ran 11 tests in 0.018s

OK
```

To run the full end-to-end simulation runner:
```bash
python generate_sample_run.py
```

---

## Menu Walkthrough & Sample Output

### 1. Digital Services Catalog
```text
==========================================================================================
ID         | SERVICE NAME                     | CATEGORY             |  PRICE ($) | STATUS  
------------------------------------------------------------------------------------------
SRV-101    | Enterprise Web Development       | Web Development      |   4,500.00 | Active  
SRV-102    | Cloud Infrastructure & DevOps    | Cloud Consulting     |   6,000.00 | Active  
SRV-103    | Mobile Application Development   | App Development      |   5,200.00 | Active  
SRV-104    | Business Intelligence & Dat...   | Data Analytics       |   3,800.00 | Active  
SRV-105    | AI & Machine Learning Integ...   | AI Solutions         |   7,500.00 | Active  
SRV-106    | Legacy System Modernization      | Enterprise IT        |   8,000.00 | Inactive
==========================================================================================
 Total Services: 6
```

### 2. Technology & Training Programs Catalog
```text
=========================================================================================================
ID         | PROGRAM NAME                       | TYPE         | DURATION   |   FEE ($) | SEATS | START DATE | STATUS   
---------------------------------------------------------------------------------------------------------
PRG-201    | Full-Stack Python & React Engi...  | Training     | 12 Weeks   |  1,200.00 |    30 | 2026-12-01 | Active   
PRG-202    | Cloud & DevOps Professional In...  | Internship   | 16 Weeks   |      FREE |    15 | 2026-12-15 | Active   
PRG-203    | Data Science & Machine Learnin...  | Training     | 10 Weeks   |  1,500.00 |    25 | 2027-01-10 | Upcoming 
PRG-204    | Enterprise Cybersecurity Funda...  | Technology   | 6 Weeks    |    950.00 |    20 | 2026-11-20 | Active   
PRG-205    | Mobile App Development with Fl...  | Internship   | 12 Weeks   |    350.00 |    18 | 2027-02-01 | Upcoming 
PRG-206    | Cobol to Microservices Transit...  | Technology   | 4 Weeks    |  1,800.00 |    10 | 2026-08-01 | Closed   
=========================================================================================================
 Total Programs: 6
```

### 3. Customer Inquiry & Service Requests
```text
===================================================================================================================
ID         | CUSTOMER             | TARGET OFFERING                | PRIORITY  | STATUS       | DATE      
-------------------------------------------------------------------------------------------------------------------
INQ-301    | Sarah Jenkins        | [S] Cloud Infrastructure ...   | High      | In Progress  | 2026-10-15
INQ-302    | David Chen           | [S] Enterprise Web Develo...   | Urgent    | Open         | 2026-10-22
INQ-303    | Priya Sharma         | [P] Data Science & Machin...   | Medium    | Open         | 2026-10-29
INQ-304    | Marcus Vance         | [S] Mobile Application De...   | Medium    | Resolved     | 2026-10-20
INQ-305    | Aisha Al-Mansoor     | [S] AI & Machine Learning...   | High      | In Progress  | 2026-11-02
INQ-306    | Ethan Walker         | [P] Cloud & DevOps Profes...   | Low       | Closed       | 2026-11-03
===================================================================================================================
 Total Inquiries: 6
```

### 4. Executive Business Summary & Revenue Analytics
```text
=================================================================
           VEDA TECHNOLOGY - EXECUTIVE BUSINESS SUMMARY          
                  Generated: 2026-11-06 12:25:49                 
=================================================================
  Total Digital Services Catalog :    7
    - Active Offerings           :    6
    - Inactive / Deprecated      :    1
-----------------------------------------------------------------
  Total Training & Tech Programs :    7
    - Active Cohorts             :    4
    - Upcoming Cohorts           :    2
    - Closed / Completed Cohorts :    1
-----------------------------------------------------------------
  Total Registered Customers     :    7
-----------------------------------------------------------------
  Total Inquiries Logged         :    7
    - Open (Pending Review)      :    2
    - In Progress                :    3
    - Resolved                   :    1
    - Closed                     :    1
=================================================================

=================================================================
            PROGRAM CAPACITY & PROJECTED REVENUE REPORT          
=================================================================
  Total Educational Programs      : 7
  Tuition-Paid Programs           : 6
  Free / Sponsored Internships    : 1
  Total Seat Capacity Across All  : 143 seats
  Average Paid Program Tuition    : $1,200.00 USD
  Total Potential Program Revenue : $151,800.00 USD
-----------------------------------------------------------------
 [Cohort Revenue Potential Breakdown]
  - Full-Stack Python & React Engi | 30 seats @ $1,200.00 = $ 36,000.00
  - Cloud & DevOps Professional In | 15 seats @      Free = $      0.00
  - Data Science & Machine Learnin | 25 seats @ $1,500.00 = $ 37,500.00
  - Enterprise Cybersecurity Funda | 20 seats @   $950.00 = $ 19,000.00
  - Mobile App Development with Fl | 18 seats @   $350.00 = $  6,300.00
  - Cobol to Microservices Transit | 10 seats @ $1,800.00 = $ 18,000.00
  - AI Agents & LLM Engineering Ma | 25 seats @ $1,400.00 = $ 35,000.00
=================================================================
```

---

## Data Storage & Sample Records

All records are stored as indented JSON in `data/`:
- `data/services.json` (6 pre-loaded synthetic services)
- `data/programs.json` (6 pre-loaded technology & internship cohorts)
- `data/customers.json` (6 pre-loaded client businesses and scholars)
- `data/inquiries.json` (6 pre-loaded customer inquiries linked to services/programs)

---

## Future Improvements

1. **Relational Database Migration**: Transition storage layer from JSON to SQLite or PostgreSQL with SQLAlchemy ORM.
2. **RESTful Web API**: Build FastAPI / Flask endpoints exposing service and program catalogs for frontend apps.
3. **Automated Notifications**: Integrate an SMTP mailer to notify customers automatically when inquiry statuses change to `In Progress` or `Resolved`.
4. **Role-Based Access Control (RBAC)**: Support separate credentials for Administrators, Sales Consultants, and Students.
5. **Interactive Dashboard**: Create a lightweight Streamlit or React web dashboard for visual charting.

---

## Git Setup & Push Instructions

To commit and push the project to GitHub at `https://github.com/hemasrimalla/veda-business-management-system`:

```bash
# 1. Navigate to the project directory
cd "C:\Users\HEMA\.gemini\antigravity\scratch\veda-business-management-system"

# 2. Check current git status
git status

# 3. Add all files to staging
git add .

# 4. Commit changes with a descriptive message
git commit -m "Refactor: Implement modular architecture for Veda Business Management System with models, managers, and full tests"

# 5. Ensure the branch is set to main
git branch -M main

# 6. Check that the remote is pointing to your GitHub repository
git remote -v
# If the remote is not set, run:
# git remote add origin https://github.com/hemasrimalla/veda-business-management-system.git

# 7. Push changes to GitHub
git push -u origin main
```
