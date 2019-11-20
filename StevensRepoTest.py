"""
This is the test file for HW12

"""

import unittest
from HW12 import University, Students, Instructors, file_reader
from prettytable import PrettyTable
from collections import defaultdict
import os


class TestStevensRepo(unittest.TestCase):
    """ Test class for the Stevens Repository System """

    def test_university_init(self):
        """ Verify if __init__ method in  University class works properly """

        Stanford = University(r'../StevensRepo', web=True)

        self.assertTrue(Stanford.directory == "../StevensRepo")
        self.assertTrue(type(Stanford.student), type(dict()))
        self.assertTrue(type(Stanford.instructor), type(dict()))
        self.assertEqual(type(Stanford.majors), type(defaultdict(lambda: defaultdict(list))))
        self.assertEqual(type(Stanford.student_data), type(list()))
        self.assertEqual(type(Stanford.instructor_data), type(list()))

    def test_university_add_student(self):
        """ Verify if add_student method in University class works properly """

        Stanford = University(r'../StevensRepo', pt=False)
        Stanford.add_student('1010', 'Shivani, T', 'SFEN')
        Stanford.add_student('1020', 'Kuhu, T', 'CS')
        Stanford.add_student('1030', 'Saurabh, D', 'MIS')

        self.assertEqual(type(Stanford.student['1010']), type(Students('1010', 'Shivani, T', 'SFEN')))
        self.assertEqual(type(Stanford.student['1020']), type(Students('1020', 'Kuhu, T', 'CS')))
        self.assertEqual(type(Stanford.student['1030']), type(Students('1030', 'Saurabh, D', 'MIS')))

    def test_university_add_instructor(self):
        """ Verify if add_instructor method in University class works properly """

        Stanford = University(r'../StevensRepo', pt=False)
        Stanford.add_instructor('1010', 'Shivani, T', 'SFEN')
        Stanford.add_instructor('1020', 'Kuhu, T', 'CS')
        Stanford.add_instructor('1030', 'Saurabh, D', 'MIS')

        self.assertEqual(type(Stanford.instructor['1010']), type(Instructors('1010', 'Shivani, T', 'SFEN')))
        self.assertEqual(type(Stanford.instructor['1020']), type(Instructors('1020', 'Kuhu, T', 'CS')))
        self.assertEqual(type(Stanford.instructor['1030']), type(Instructors('1030', 'Saurabh, D', 'MIS')))

    def test_student_init(self):
        """ Verify if __init__ method in Student class works properly """

        student1 = Students('1010', 'Shivani, T', 'SFEN')

        self.assertEqual(student1.name, 'Shivani, T')
        self.assertEqual(student1.major, 'SFEN')
        self.assertEqual(student1.cwid, '1010')
        self.assertEqual(type(student1.courses), type(defaultdict()))
        self.assertEqual(type(student1.remaining_required), type(list()))
        self.assertEqual(type(student1.remaining_electives), type(list()))

        student2 = Students('1020', 'Kuhu, T', 'CS')
        self.assertEqual(student2.name, 'Kuhu, T')
        self.assertEqual(student2.major, 'CS')
        self.assertEqual(student2.cwid, '1020')
        self.assertEqual(type(student2.courses), type(defaultdict()))
        self.assertEqual(type(student2.remaining_required), type(list()))
        self.assertEqual(type(student2.remaining_electives), type(list()))

    def test_student_add_course(self):
        """ Verify if add_course method in Student class works properly """

        student1 = Students('1010', 'Shivani, T', 'SFEN')
        student1.add_course('SSW 810', 'A')
        student1.add_course('SSW 540', 'C')
        student1.add_course('SSW 564', 'F')

        self.assertEqual(len(student1.courses), 2)

        student2 = Students('1020', 'Akash, D', 'SYEN')
        student2.add_course('SSW 540', 'C')
        student2.add_course('SYS 650', 'F')
        student2.add_course('SSW 564', '')

        self.assertEqual(len(student2.courses), 1)

    def test_student_update_course(self):
        """ Verify if update_course method works properly """

        Stevens = University(r'../StevensRepo', pt=False)
        student = Students('1010', 'Shivani, T', 'SFEN')
        student.add_course('SSW 689', 'A')
        student.update_course(Stevens.majors)

        expected_required = ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567']
        expected_electives = ['CS 501', 'CS 513', 'CS 545']

        self.assertEqual(student.remaining_required, expected_required)
        self.assertEqual(student.remaining_electives, expected_electives)

    def test_student_pt_row(self):
        """ Verify if pt_row method works properly """

        Stevens = University(r'../StevensRepo', pt=False)
        student = Students('1010', 'Shivani, T', 'SFEN')
        student.add_course('SSW 689', 'A')
        student.update_course(Stevens.majors)

        self.assertEqual(
            [student.cwid, student.name, student.major, sorted(list(student.courses)), student.remaining_required,
             student.remaining_electives], student.pt_row())

    def test_instructor_init(self):
        """ Verify if __init__ method in Instructor class works properly """

        instructor = Instructors('1010', 'Shivani, T', 'SFEN')
        self.assertEqual(instructor.name, 'Shivani, T')
        self.assertEqual(instructor.department, 'SFEN')
        self.assertEqual(type(instructor.prof_course), type(defaultdict()))

    def test_instructor_course_taught(self):
        """ Verify if add_course method in Instructor class works properly """

        instructor = Instructors('98765', 'Shivani, T', 'SFEN')
        instructor.course_taught('SSW 810')
        instructor.course_taught('SSW 810')
        instructor.course_taught('SSW 564')
        self.assertTrue(instructor.prof_course['SSW 810'] == 2)
        self.assertTrue(instructor.prof_course['SSW 564'] == 1)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
