# Human Resource Management System

A comprehensive HR solution built in Python specifically designed for Malaysian businesses, featuring automated salary calculations with EPF, SOCSO, and SIP deductions, intelligent staff scheduling, and leave management.

## 🌟 Features

### 1. Automated Salary Slip Generation
- **Base Salary**: RM 1,700 default base salary
- **Malaysian Deductions**: 
  - EPF (Employee Provident Fund): 11% employee, 12% employer
  - SOCSO (Social Security): 0.5% employee, 1.75% employer  
  - SIP (Employment Insurance): 0.2% employee
- **Overtime Calculation**: 1.5x base rate for overtime hours
- **Special Holiday Pay**: 2x base rate for special holiday work
- **Automatic PDF/Text Generation**: Formatted salary slips saved automatically

### 2. Intelligent Staff Scheduling
- **Shift Management**: Three shifts (7am-3pm, 3pm-11pm, 11pm-7am)
- **Position-Based Scheduling**:
  - 2 Cashiers per shift (all shifts)
  - 2 Forecourt Staff per shift (day and evening only)
- **Automatic Staff Allocation**: Fair distribution of shifts among available staff
- **Shortage Detection**: Automatically flags understaffing situations

### 3. Leave Management & Automatic Reallocation
- **Leave Request System**: Submit and track leave requests
- **Automatic Reallocation**: System automatically reassigns staff when colleagues are on leave
- **Conflict Resolution**: Identifies and resolves scheduling conflicts
- **Leave Balance Tracking**: Monitor leave entitlements and usage

## 📁 Project Structure

```
hr_management_system/
│
├── main.py                 # Main application entry point
├── salary_calculator.py    # Salary calculation and slip generation
├── schedule_manager.py     # Staff scheduling and reallocation
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
│
├── data/                  # Data storage directory
│   ├── employees.json     # Employee database
│   ├── leave_requests.json # Leave requests data
│   └── schedules.json     # Generated schedules
│
├── salary_slips/          # Generated salary slips
│   └── [employee_id]_[month].txt
│
└── reports/               # Generated reports and analytics
    └── schedule_reports/
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external dependencies required for basic functionality

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   git clone [repository-url]
   cd hr_management_system
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv hr_env
   source hr_env/bin/activate  # On Windows: hr_env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### Adding Employees
1. Run the main application
2. Select "Add Employee" from the menu
3. Enter employee details:
   - Employee ID (unique identifier)
   - Name
   - Position (Cashier or Forecourt Staff)

### Generating Salary Slips
1. Select "Generate Salary Slip" from menu
2. Enter:
   - Employee ID
   - Month (YYYY-MM format)
   - Overtime hours (if any)
   - Special holiday hours (if any)
3. System automatically calculates and generates formatted salary slip

### Creating Work Schedules
1. Select "Generate Schedule" from menu
2. Enter start date (YYYY-MM-DD format)
3. Specify number of days (default: 7)
4. System automatically assigns staff based on:
   - Position requirements
   - Staff availability
   - Leave requests
   - Fair distribution principles

### Managing Leave Requests
1. **Submit Leave**: Select "Request Leave" and provide dates and reason
2. **View Requests**: Monitor all leave requests and their status
3. **Automatic Reallocation**: System automatically adjusts schedules when leave is approved

## 🔧 Configuration

### Salary Settings
Edit `salary_calculator.py` to modify:
- Base salary amounts
- Overtime rates
- Deduction percentages
- Holiday pay rates

### Shift Requirements
Edit `schedule_manager.py` to modify:
- Shift times
- Staff requirements per shift
- Position-specific scheduling rules

### Malaysian Compliance
The system is pre-configured with current Malaysian employment regulations:
- EPF rates and ceilings
- SOCSO contribution tables
- SIP rates and limits

## 📊 Key Classes and Methods

### Main HR System (`main.py`)
- `HRSystem`: