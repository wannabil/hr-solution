# salary_calculator.py - Salary Calculation with Malaysian Deductions
from datetime import datetime
from typing import Dict, Tuple

class MalaysianDeductions:
    """Malaysian EPF, SOCSO, and SIP calculation according to current rates"""
    
    @staticmethod
    def calculate_epf(gross_salary: float) -> Tuple[float, float]:
        """Calculate EPF deduction (Employee: 11%, Employer: 12%)"""
        if gross_salary <= 20.0:
            return 0.0, 0.0
        
        # EPF contribution ceiling is RM5000
        contributory_salary = min(gross_salary, 5000.0)
        employee_epf = contributory_salary * 0.11
        employer_epf = contributory_salary * 0.12
        
        return employee_epf, employer_epf
    
    @staticmethod
    def calculate_socso(gross_salary: float) -> Tuple[float, float]:
        """Calculate SOCSO deduction based on contribution table"""
        if gross_salary <= 30.0:
            return 0.0, 0.0
        
        # SOCSO contribution ceiling is RM4000
        if gross_salary > 4000.0:
            return 19.75, 33.40  # Maximum contribution
        
        # Simplified SOCSO calculation (actual uses detailed table)
        employee_socso = gross_salary * 0.005  # 0.5%
        employer_socso = gross_salary * 0.0175  # 1.75%
        
        return round(employee_socso, 2), round(employer_socso, 2)
    
    @staticmethod
    def calculate_sip(gross_salary: float) -> float:
        """Calculate SIP (Employment Insurance) - Employee only pays"""
        if gross_salary <= 30.0:
            return 0.0
        
        # SIP contribution ceiling is RM4000
        contributory_salary = min(gross_salary, 4000.0)
        employee_sip = contributory_salary * 0.002  # 0.2%
        
        return round(employee_sip, 2)

class SalaryCalculator:
    def __init__(self):
        self.deductions = MalaysianDeductions()
    
    def calculate_overtime_pay(self, base_salary: float, overtime_hours: float) -> float:
        """Calculate overtime pay at 1.5x rate"""
        hourly_rate = base_salary / (30 * 8)  # Assuming 30 days, 8 hours per day
        return overtime_hours * hourly_rate * 1.5
    
    def calculate_special_holiday_pay(self, base_salary: float, special_hours: float) -> float:
        """Calculate special holiday pay at 2x rate"""
        hourly_rate = base_salary / (30 * 8)
        return special_hours * hourly_rate * 2.0
    
    def generate_salary_slip(self, employee, month: str, overtime_hours: float = 0, 
                           special_holiday_hours: float = 0) -> str:
        """Generate complete salary slip"""
        
        # Basic calculations
        base_salary = employee.base_salary
        overtime_pay = self.calculate_overtime_pay(base_salary, overtime_hours)
        special_pay = self.calculate_special_holiday_pay(base_salary, special_holiday_hours)
        gross_salary = base_salary + overtime_pay + special_pay
        
        # Malaysian deductions
        employee_epf, employer_epf = self.deductions.calculate_epf(gross_salary)
        employee_socso, employer_socso = self.deductions.calculate_socso(gross_salary)
        employee_sip = self.deductions.calculate_sip(gross_salary)
        
        total_deductions = employee_epf + employee_socso + employee_sip
        net_salary = gross_salary - total_deductions
        
        # Generate salary slip
        slip = f"""
{'='*60}
                    SALARY SLIP
{'='*60}
Employee ID    : {employee.id}
Employee Name  : {employee.name}
Position       : {employee.position.value}
Month          : {month}
Generated Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
                    EARNINGS
{'='*60}
Base Salary              : RM {base_salary:,.2f}
Overtime Pay ({overtime_hours:,.1f} hrs)  : RM {overtime_pay:,.2f}
Special Holiday ({special_holiday_hours:,.1f} hrs): RM {special_pay:,.2f}
                          ----------------
GROSS SALARY             : RM {gross_salary:,.2f}

{'='*60}
                   DEDUCTIONS
{'='*60}
EPF (Employee 11%)       : RM {employee_epf:,.2f}
SOCSO (Employee 0.5%)    : RM {employee_socso:,.2f}
SIP (Employee 0.2%)      : RM {employee_sip:,.2f}
                          ----------------
TOTAL DEDUCTIONS         : RM {total_deductions:,.2f}

{'='*60}
NET SALARY               : RM {net_salary:,.2f}
{'='*60}

EMPLOYER CONTRIBUTIONS:
EPF (Employer 12%)       : RM {employer_epf:,.2f}
SOCSO (Employer 1.75%)   : RM {employer_socso:,.2f}

Note: This salary slip is generated automatically by HR System.
All calculations are based on current Malaysian employment regulations.
"""
        
        # Save salary slip to file
        import os
        os.makedirs('salary_slips', exist_ok=True)
        filename = f"salary_slips/{employee.id}_{month.replace('-', '_')}.txt"
        
        with open(filename, 'w') as f:
            f.write(slip)
        
        print(f"Salary slip saved to: {filename}")
        return slip

# Example usage and testing
if __name__ == "__main__":
    from main import Employee, Position
    
    # Test salary calculation
    test_employee = Employee("E001", "Ahmad bin Ali", Position.CASHIER, 1700.0)
    calculator = SalaryCalculator()
    
    # Generate test salary slip
    salary_slip = calculator.generate_salary_slip(
        test_employee, 
        "2024-06", 
        overtime_hours=10, 
        special_holiday_hours=8
    )
    
    print(salary_slip)