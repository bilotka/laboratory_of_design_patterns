#Варіант  6. Система містить записи про університети, які можуть складатись із факультетів, які, в свою чергу,   складаються із 
# кафедр, на яких працюють викладачі, доценти та професори. Для кожного працівника відомий його стаж та заробітна плата.
#а) підрахувати скільки коштів потрібно для виплати заробітної плати на кожному університеті, факультеті,  кафедрі.
#б)  всім працівникам, у яких стаж перевищує Х років збільшити заробітну плату на  У
# %Врахувати можливість в майбутньому додавання інших операцій
from __future__ import annotations
from typing import Protocol, List
from dataclasses import dataclass

class IVisitor(Protocol):
    def visit(self, target: "IVisitable"): ...


class IVisitable(Protocol):
    def accept(self, visitor: IVisitor): ...

@dataclass
class Professor(IVisitable):
    name: str
    experience_years: int
    salary: float

    def accept(self, visitor: IVisitor):
        return visitor.visit(self)

@dataclass
class Department(IVisitable):
    name: str
    employees: List[Professor]

    def accept(self, visitor: IVisitor):
        return visitor.visit(self)

@dataclass
class Faculty(IVisitable):
    name: str
    departments: List[Department]

    def accept(self, visitor: IVisitor):
        return visitor.visit(self)

@dataclass
class University(IVisitable):
    name: str
    faculties: List[Faculty]

    def accept(self, visitor: IVisitor):
        return visitor.visit(self)

class SalaryCalculator(IVisitor):
    def __init__(self):
        self.result: dict[str, float] = {}

    def visit(self, target):
        match target:
            case University(name=name, faculties=faculties):
                total = sum(f.accept(self) or 0 for f in faculties)
                self.result[name] = total
                return total

            case Faculty(name=name, departments=departments):
                total = sum(d.accept(self) or 0 for d in departments)
                self.result[name] = total
                return total

            case Department(name=name, employees=employees):
                total = sum(p.accept(self) or 0 for p in employees)
                self.result[name] = total
                return total

            case Professor(salary=s):
                return s

            case _:
                return 0.0

class SalaryIncreaseVisitor(IVisitor):
    def __init__(self, min_exp: int, percent: float):
        self.min_exp = min_exp
        self.percent = percent / 100.0

    def visit(self, target):
        match target:
            case University(faculties=faculties):
                for f in faculties:
                    f.accept(self)

            case Faculty(departments=departments):
                for d in departments:
                    d.accept(self)

            case Department(employees=employees):
                for p in employees:
                    p.accept(self)

            case Professor() as p:
                if p.experience_years > self.min_exp:
                    p.salary *= (1 + self.percent)

if __name__ == "__main__":
    dep_system_analysis = Department("System Analysis Department", [
        Professor("Mykola Mykolayovych", 5, 20000),
        Professor("Myroslava Mihailovich", 12, 25000),
    ])

    dep_algebra = Department("Algebra Department", [
        Professor("Anna Andriivna", 9, 30000),
        Professor("Oleg Olegovych", 15, 40000),
    ])

    faculty_math = Faculty("Math Faculty", [dep_system_analysis, dep_algebra])
    uni = University("Uzhnu", [faculty_math])

    calc1 = SalaryCalculator()
    uni.accept(calc1)
    print("До підвищення:", calc1.result)

    inc = SalaryIncreaseVisitor(10, 10)
    uni.accept(inc)

    calc2 = SalaryCalculator()
    uni.accept(calc2)
    print("Після підвищення:", calc2.result)