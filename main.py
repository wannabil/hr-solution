# main.py - Human Resource Management System
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class Position(Enum):
    CASHIER = "Cashier"
    FORECOURT = "Forecourt Staff"

class Shift(Enum):
    MORNING = "7am-3pm"
    EVENING = "3pm-11pm" 
    NIGHT = "11pm-7am"

@dataclass
class Employee:
    id: str
    name: str
    position: Position
    base_salary: float = 1700.0
    phone: str = ""
    email: str = ""
    hire_date: str = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position.value,
            'base_salary': self.base_salary,
            'phone': self.phone,
            'email': self.email,
            'hire_date': self.hire_date
        }

@dataclass
class LeaveRequest:
    employee_id: str
    start_date: str
    end_date: str
    reason: str
    status: str = "pending"

class HRSystem:
    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.leave_requests: List[LeaveRequest] = []
        self.schedule: Dict[str, Dict[str, List[str]]] = {}
        self.load_data()
    
    def load_data(self):
        """Load existing data from JSON files"""
        try:
            if os.path.exists('data/employees.json'):
                with open('data/employees.json', 'r') as f:
                    data = json.load(f)
                    for emp_data in data:
                        emp = Employee(
                            id=emp_data['id'],
                            name=emp_data['name'],
                            position=Position(emp_data['position']),
                            base_salary=emp_data.get('base_salary', 1700.0),
                            phone=emp_data.get('phone', ''),
                            email=emp_data.get('email', ''),
                            hire_date=emp_data.get('hire_date', '')
                        )
                        self.employees[emp.id] = emp
        except Exception as e:
            print(f"Error loading employee data: {e}")
    
    def save_data(self):
        """Save data to JSON files"""
        os.makedirs('data', exist_ok=True)
        
        # Save employees
        emp_data = [emp.to_dict() for emp in self.employees.values()]
        with open('data/employees.json', 'w') as f:
            json.dump(emp_data, f, indent=2)
        
        # Save leave requests
        leave_data = [asdict(req) for req in self.leave_requests]
        with open('data/leave_requests.json', 'w') as f:
            json.dump(leave_data, f, indent=2)
    
    def add_employee(self, employee: Employee):
        """Add new employee"""
        self.employees[employee.id] = employee
        self.save_data()
        print(f"Employee {employee.name} added successfully!")
    
    def generate_schedule(self, start_date: str, days: int = 7):
        """Generate work schedule for specified period"""
        from schedule_manager import ScheduleManager
        manager = ScheduleManager(self.employees)
        return manager.generate_schedule(start_date, days, self.leave_requests)
    
    def process_salary(self, employee_id: str, month: str, overtime_hours: float = 0, 
                      special_holiday_hours: float = 0):
        """Generate salary slip for employee"""
        from salary_calculator import SalaryCalculator
        if employee_id not in self.employees:
            print("Employee not found!")
            return None
        
        calculator = SalaryCalculator()
        return calculator.generate_salary_slip(
            self.employees[employee_id], month, overtime_hours, special_holiday_hours
        )
    
    def request_leave(self, employee_id: str, start_date: str, end_date: str, reason: str):
        """Submit leave request"""
        if employee_id not in self.employees:
            print("Employee not found!")
            return
        
        leave_request = LeaveRequest(employee_id, start_date, end_date, reason)
        self.leave_requests.append(leave_request)
        self.save_data()
        print("Leave request submitted successfully!")
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("   HUMAN RESOURCE MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Employee")
        print("2. View All Employees") 
        print("3. Generate Salary Slip")
        print("4. Generate Schedule")
        print("5. Request Leave")
        print("6. View Leave Requests")
        print("7. Exit")
        print("="*50)

def main():
    hr_system = HRSystem()
    
    while True:
        hr_system.show_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            # Add Employee
            emp_id = input("Employee ID: ")
            name = input("Name: ")
            print("Positions: 1-Cashier, 2-Forecourt Staff")
            pos_choice = input("Position (1/2): ")
            position = Position.CASHIER if pos_choice == '1' else Position.FORECOURT
            
            employee = Employee(emp_id, name, position)
            hr_system.add_employee(employee)
        
        elif choice == '2':
            # View Employees
            print("\n--- EMPLOYEE LIST ---")
            for emp in hr_system.employees.values():
                print(f"ID: {emp.id} | Name: {emp.name} | Position: {emp.position.value}")
        
        elif choice == '3':
            # Generate Salary Slip
            emp_id = input("Employee ID: ")
            month = input("Month (YYYY-MM): ")
            overtime = float(input("Overtime hours (0 if none): ") or "0")
            special = float(input("Special holiday hours (0 if none): ") or "0")
            
            salary_slip = hr_system.process_salary(emp_id, month, overtime, special)
            if salary_slip:
                print("\n" + salary_slip)
        
        elif choice == '4':
            # Generate Schedule
            start_date = input("Start date (YYYY-MM-DD): ")
            days = int(input("Number of days (default 7): ") or "7")
            
            schedule = hr_system.generate_schedule(start_date, days)
            print("\n--- WORK SCHEDULE ---")
            for date, shifts in schedule.items():
                print(f"\nDate: {date}")
                for shift, staff in shifts.items():
                    print(f"  {shift}: {', '.join(staff) if staff else 'No staff assigned'}")
        
        elif choice == '5':
            # Request Leave
            emp_id = input("Employee ID: ")
            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")
            reason = input("Reason: ")
            
            hr_system.request_leave(emp_id, start_date, end_date, reason)
        
        elif choice == '6':
            # View Leave Requests
            print("\n--- LEAVE REQUESTS ---")
            for req in hr_system.leave_requests:
                emp_name = hr_system.employees.get(req.employee_id, {}).name if req.employee_id in hr_system.employees else "Unknown"
                print(f"Employee: {emp_name} | Dates: {req.start_date} to {req.end_date} | Status: {req.status}")
        
        elif choice == '7':
            print("Thank you for using HR Management System!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()