"""
Author: @Shivani Taneja
Class definitions: University, Student, Instructor

"""

from collections import defaultdict
from prettytable import PrettyTable
import os
import sqlite3


class University:
    """ University Class to process and store student and instructor information """

    def __init__(self, directory, pt=False, web=True):
        """ Initialise university repository """

        self.directory = directory
        os.chdir(self.directory)
        self.student = dict()
        self.instructor = dict()
        self.majors = defaultdict(lambda: defaultdict(list))
        self.student_sum = PrettyTable()
        self.instructor_sum = PrettyTable()
        self.majors_sum = PrettyTable()
        self.student_data = list()
        self.instructor_data = list()
        cwd = os.getcwd()

        if not os.path.exists(self.directory):
            raise FileNotFoundError

        file1 = 'students.txt'
        path1 = os.path.join(cwd, file1)
        for cwid, name, major in file_reader(path1, fields=3, seperator='\t'):
            self.add_student(cwid, name, major)

        file2 = 'instructors.txt'
        path2 = os.path.join(cwd, file2)
        for instructor_cwid, instructor_name, department in file_reader(path2, fields=3, seperator='\t'):
            self.add_instructor(instructor_cwid, instructor_name, department)

        file3 = 'grades.txt'
        path3 = os.path.join(cwd, file3)
        for cwid, course_name, grades, instructor_cwid in file_reader(path3, fields=4, seperator='|'):
            for key1, value1 in self.student.items():
                if key1 == cwid:
                    self.student[cwid].add_course(course_name, grades)

            for key2, value2 in self.instructor.items():
                if key2 == instructor_cwid:
                    self.instructor[instructor_cwid].course_taught(course_name)

        file4 = 'majors.txt'
        path4 = os.path.join(cwd, file4)
        for major, flag, course in file_reader(path4, fields=3, seperator='\t'):
            self.majors[major][flag].append(course)

        if pt:
            self.majors_sum.add_column("Department", [dept for dept in self.majors.keys()])
            self.majors_sum.add_column("Required", [i['R'] for i in self.majors.values()])
            self.majors_sum.add_column("Electives", [i['E'] for i in self.majors.values()])

            self.student_sum.field_names = Students.fields
            for studs in self.student.values():
                studs.update_course(self.majors)
                self.student_sum.add_row(studs.pt_row())

            self.instructor_sum.field_names = Instructors.fields
            for inst in self.instructor.values():
                for i in inst.pt_row():
                    self.instructor_sum.add_row(i)

            print(f"Majors Summary: \n{self.majors_sum}")
            print(f"Student Summary: \n{self.student_sum}")
            print(f"Instructor Summary: \n{self.instructor_sum}")

        if web:
            DB_FILE = os.path.join(cwd, 'Stevens.db')
            db = sqlite3.connect(DB_FILE)

            student_query = """ select s.cwid, s.name, s.major, count(g.Course) as complete
                        from student_table s join grade_table g on s.cwid=g.Student_CWID
                        group by s.cwid, s.name, s.major """

            self.student_data = [{'cwid': cwid, 'name': name, 'major': major, 'complete': complete}
                                 for cwid, name, major, complete in db.execute(student_query)]

            instructor_query = """ select i.CWID, i.Name, i.Dept, g.Course, count(*) as Students
                        from instructor_table i
                        join grade_table g on i.CWID=g.Instructor_CWID
                        group by g.Course order by i.CWID ASC """

            self.instructor_data = [{'cwid': cwid, 'name': name, 'dept': dept, 'courses': courses, 'students': students}
                                    for cwid, name, dept, courses, students in db.execute(instructor_query)]

            db.close()

    def add_student(self, cwid, name, major):
        """ Class method to add a student into the univeristy repository """

        self.student[cwid] = Students(cwid, name, major)

    def add_instructor(self, cwid, name, department):
        """ Class method to add an instructor into the university repository """

        self.instructor[cwid] = Instructors(cwid, name, department)


class Students:
    """ Student Class to initialize student information, add courses and display student information """

    fields = ["CWID", "Name", "Major", "Courses", "Remaining Required", "Remaining Electives"]

    def __init__(self, cwid, name, major):
        """ Initialise student as object with name, major, and courses as attributes """

        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = defaultdict(str)
        self.remaining_required = list()
        self.remaining_electives = list()

    def add_course(self, subj, *grade):
        """ Class method to add a course and grade """

        valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        {self.courses[subj]: i for i in grade if i in valid_grades}

    def update_course(self, majors):
        """ Class method to update student program requirements """

        for i in majors[self.major]['R']:  # required_courses
            if i not in self.courses:
                self.remaining_required.append(i)

        for j in majors[self.major]['E']:  # elective_courses
            if j in self.courses:
                self.remaining_electives = None
                break

            else:
                self.remaining_electives.append(j)

    def pt_row(self):
        """ Class method for Pretty Table """

        return [self.cwid, self.name, self.major, sorted(list(self.courses)), self.remaining_required,
                self.remaining_electives]


class Instructors:
    """ Instructor class to initialise instructor information, add courses taught and display instructor information """

    fields = ["CWID", "Name", "Department", "Course Name", "No. of Students"]

    def __init__(self, instructor_cwid, instructor_name, department):
        """ Initialise instructor as an object with instructor name, department and courses taught as attributes """

        self.cwid = instructor_cwid
        self.name = instructor_name
        self.department = department
        self.prof_course = defaultdict(int)

    def course_taught(self, subj):
        """Class method to add a course taught and count the number of students """

        self.prof_course[subj] += 1

    def pt_row(self):
        """ Class method for Pretty Table """

        new_list = []
        if len(self.prof_course) != 0:
            for key, value in self.prof_course.items():
                new_list.append([self.cwid, self.name, self.department, key, value])

        return new_list


def file_reader(path, fields, seperator=',', header=False):
    """ File Reader Function to clean a field separated file """

    try:
        fp = open(path, 'r')

    except FileNotFoundError:
        print(f"Cant Open: {path}")

    else:
        with fp:
            if header:
                next(fp)

            for num, line in enumerate(fp, 1):
                line = line.strip()

                if line.count(seperator) == fields - 1:
                    yield tuple(line.split(seperator))

                else:
                    raise ValueError(
                        f"{path} has {line.count(seperator) + 1} fields on line {num} but expected {fields} fields")


def main():
    """ Main Function to interact with the user """

    Stevens = University(r'../StevensRepo', web=False, pt=True)


if __name__ == '__main__':
    main()
