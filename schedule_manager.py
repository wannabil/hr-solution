# schedule_manager.py - Automated Staff Scheduling System
from datetime import datetime, timedelta
from typing import Dict, List, Set
import random
from collections import defaultdict
from main import Position, Shift

class ScheduleManager:
    def __init__(self, employees: Dict):
        self.employees = employees
        self.cashiers = [emp for emp in employees.values() if emp.position == Position.CASHIER]
        self.forecourt_staff = [emp for emp in employees.values() if emp.position == Position.FORECOURT]
        
        # Shift requirements
        self.shift_requirements = {
            Shift.MORNING.value: {"cashier": 2, "forecourt": 2},
            Shift.EVENING.value: {"cashier": 2, "forecourt": 2}, 
            Shift.NIGHT.value: {"cashier": 2, "forecourt": 0}  # No forecourt at night
        }
    
    def get_employees_on_leave(self, date_str: str, leave_requests: List) -> Set[str]:
        """Get list of employees on leave for a specific date"""
        employees_on_leave = set()
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        for leave in leave_requests:
            if leave.status == "approved":
                start_date = datetime.strptime(leave.start_date, '%Y-%m-%d')
                end_date = datetime.strptime(leave.end_date, '%Y-%m-%d')
                
                if start_date <= target_date <= end_date:
                    employees_on_leave.add(leave.employee_id)
        
        return employees_on_leave
    
    def get_available_staff(self, position: Position, employees_on_leave: Set[str]) -> List:
        """Get available staff for a position, excluding those on leave"""
        if position == Position.CASHIER:
            return [emp for emp in self.cashiers if emp.id not in employees_on_leave]
        else:
            return [emp for emp in self.forecourt_staff if emp.id not in employees_on_leave]
    
    def assign_shift_staff(self, available_cashiers: List, available_forecourt: List, 
                          shift: str, date: str) -> Dict[str, List[str]]:
        """Assign staff to a specific shift with automatic reallocation"""
        assignment = {"cashier": [], "forecourt": []}
        requirements = self.shift_requirements[shift]
        
        # Assign cashiers
        needed_cashiers = requirements["cashier"]
        if len(available_cashiers) >= needed_cashiers:
            selected_cashiers = random.sample(available_cashiers, needed_cashiers)
            assignment["cashier"] = [emp.name for emp in selected_cashiers]
        else:
            # Not enough cashiers - assign all available and flag shortage
            assignment["cashier"] = [emp.name for emp in available_cashiers]
            shortage = needed_cashiers - len(available_cashiers)
            assignment["cashier"].append(f"[SHORTAGE: {shortage} cashier(s) needed]")
        
        # Assign forecourt staff (if needed for this shift)
        needed_forecourt = requirements["forecourt"]
        if needed_forecourt > 0:
            if len(available_forecourt) >= needed_forecourt:
                selected_forecourt = random.sample(available_forecourt, needed_forecourt)
                assignment["forecourt"] = [emp.name for emp in selected_forecourt]
            else:
                # Not enough forecourt staff - assign all available and flag shortage
                assignment["forecourt"] = [emp.name for emp in available_forecourt]
                shortage = needed_forecourt - len(available_forecourt)
                assignment["forecourt"].append(f"[SHORTAGE: {shortage} forecourt staff needed]")
        
        return assignment
    
    def generate_schedule(self, start_date: str, days: int, leave_requests: List) -> Dict:
        """Generate complete schedule with automatic staff reallocation"""
        schedule = {}
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        
        # Track staff assignments to ensure fair distribution
        staff_shift_count = defaultdict(int)
        
        for day in range(days):
            current_date = start_dt + timedelta(days=day)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Get employees on leave for this date
            employees_on_leave = self.get_employees_on_leave(date_str, leave_requests)
            
            # Get available staff (excluding those on leave)
            available_cashiers = self.get_available_staff(Position.CASHIER, employees_on_leave)
            available_forecourt = self.get_available_staff(Position.FORECOURT, employees_on_leave)
            
            # Initialize daily schedule
            schedule[date_str] = {}
            
            # Assign staff for each shift
            shifts = [Shift.MORNING.value, Shift.EVENING.value, Shift.NIGHT.value]
            
            for shift in shifts:
                assignment = self.assign_shift_staff(
                    available_cashiers, available_forecourt, shift, date_str
                )
                
                # Combine cashier and forecourt assignments for display
                shift_staff = []
                if assignment["cashier"]:
                    cashier_list = ", ".join(assignment["cashier"])
                    shift_staff.append(f"Cashiers: {cashier_list}")
                
                if assignment["forecourt"]:
                    forecourt_list = ", ".join(assignment["forecourt"])
                    shift_staff.append(f"Forecourt: {forecourt_list}")
                
                schedule[date_str][shift] = shift_staff
                
                # Update staff shift counts for fair distribution
                for cashier in assignment["cashier"]:
                    if not cashier.startswith("[SHORTAGE"):
                        staff_shift_count[cashier] += 1
                        
                for forecourt in assignment["forecourt"]:
                    if not forecourt.startswith("[SHORTAGE"):
                        staff_shift_count[forecourt] += 1
        
        # Add summary information
        schedule["_summary"] = {
            "total_days": days,
            "start_date": start_date,
            "end_date": (start_dt + timedelta(days=days-1)).strftime('%Y-%m-%d'),
            "total_cashiers": len(self.cashiers),
            "total_forecourt_staff": len(self.forecourt_staff),
            "staff_shift_distribution": dict(staff_shift_count)
        }
        
        return schedule
    
    def generate_weekly_schedule(self, start_date: str) -> Dict:
        """Generate a standard weekly schedule"""
        return self.generate_schedule(start_date, 7, [])
    
    def print_schedule_summary(self, schedule: Dict):
        """Print a formatted schedule summary"""
        print("\n" + "="*80)
        print("                    WORK SCHEDULE SUMMARY")
        print("="*80)
        
        if "_summary" in schedule:
            summary = schedule["_summary"]
            print(f"Period: {summary['start_date']} to {summary['end_date']}")
            print(f"Total Staff: {summary['total_cashiers']} Cashiers, {summary['total_forecourt_staff']} Forecourt")
            print("-" * 80)
        
        for date, shifts in schedule.items():
            if date.startswith("_"):  # Skip summary data
                continue
                
            print(f"\n📅 {date} ({datetime.strptime(date, '%Y-%m-%d').strftime('%A')})")
            print("-" * 40)
            
            for shift, staff_assignments in shifts.items():
                print(f"  ⏰ {shift}:")
                if staff_assignments:
                    for assignment in staff_assignments:
                        print(f"    • {assignment}")
                else:
                    print("    • No staff assigned")
        
        print("\n" + "="*80)

# Standalone testing and utilities
class ScheduleTester:
    @staticmethod
    def create_test_employees():
        """Create test employees for demonstration"""
        from main import Employee, Position
        
        employees = {
            "C001": Employee("C001", "Ahmad Ali", Position.CASHIER),
            "C002": Employee("C002", "Siti Nor", Position.CASHIER),
            "C003": Employee("C003", "Raj Kumar", Position.CASHIER),
            "C004": Employee("C004", "Lee Ming", Position.CASHIER),
            "C005": Employee("C005", "Fatimah", Position.CASHIER),
            "F001": Employee("F001", "Hassan", Position.FORECOURT),
            "F002": Employee("F002", "Kumar", Position.FORECOURT),
            "F003": Employee("F003", "Wong", Position.FORECOURT),
            "F004": Employee("F004", "Ali", Position.FORECOURT),
        }
        return employees
    
    @staticmethod
    def test_schedule_generation():
        """Test the schedule generation system"""
        employees = ScheduleTester.create_test_employees()
        manager = ScheduleManager(employees)
        
        # Generate test schedule
        schedule = manager.generate_schedule("2024-06-16", 7, [])
        manager.print_schedule_summary(schedule)
        
        return schedule

if __name__ == "__main__":
    # Run tests
    print("Testing Schedule Manager...")
    ScheduleTester.test_schedule_generation()