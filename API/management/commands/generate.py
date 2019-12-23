from multiprocessing import Pool, cpu_count
import os
import random

from django.core.management.base import BaseCommand
from API.models import StudentMarks, SemesterDetails, StudentDetails
from contextlib import closing

from django.db import connection


class Student:
    def __init__(self, student_id, semester, grade, year):
        try:
            req = {
                'student_id': f'std_id{student_id}',
                'student_name': f'student-{student_id}'
            }

            student_obj = StudentDetails.objects.filter(**req)
            if not student_obj.exists():
                student_obj = StudentDetails.objects.create(**req).save()
            student_obj = StudentDetails.objects.get_or_create(**req)
            self.student, _ = student_obj

            req = {
                'semester': semester,
                'grade': grade,
                'calendar_year': year
            }

            semester_obj = SemesterDetails.objects.filter(**req)
            if not semester_obj.exists():
                SemesterDetails.objects.create(**req).save()
            semester_obj = SemesterDetails.objects.get_or_create(**req)
            self.semester, _ = semester_obj
        except Exception as e:
            print(e)
            print(f'__init__ | {os.getpid()} | {os.getppid()} -> ERROR')

    def generate_semester_data(self):
        # print(f'generate_semester_data | {os.getpid()} | {os.getppid()} -> START')
        try:
            sem = self.semester.semester
            return [
                (f"('sem_{sem}_sub_{subject_id}', "
                 f"{random.randint(0, 100)}, "
                 f"{self.semester.id}, "
                 f"{self.student.id})")
                for subject_id in range(1, 25001)]
        except Exception as e:
            print(e)
            print(f'generate_semester_data | {os.getpid()} | {os.getppid()} -> ERROR')


class Command(BaseCommand):
    @staticmethod
    def handle_student(student_id):
        try:
            full_obj_list = []
            semester_count = 2  # semesters in a year
            print(f'{student_id} | {os.getpid()} | {os.getppid()} -> START')
            for grade, year in enumerate(range(2000, 2010), start=1):
                year_obj_list = []
                for semester in range(1, semester_count + 1):
                    student = Student(student_id, semester, grade, year)
                    year_obj_list = year_obj_list + student.generate_semester_data()
                full_obj_list = full_obj_list + year_obj_list
            print(f'{student_id} | {os.getpid()} | {os.getppid()} -> DONE')
            sql = "INSERT INTO API_studentmarks (subject_name, mark, semester_id, student_id) VALUES "
            val = ", ".join(full_obj_list)
            with closing(connection.cursor()) as cursor:
                cursor.execute(f'{sql}{val}')
            return full_obj_list
        except Exception as e:
            print(e)
            print(f'handle_student | {os.getpid()} | {os.getppid()} -> ERROR')

    def handle(self, *args, **kwargs):
        StudentMarks.objects.all().delete()
        SemesterDetails.objects.all().delete()
        StudentDetails.objects.all().delete()
        student_list = [i for i in range(1, 20)]
        with Pool(cpu_count()) as p:
            all_data = p.map(self.handle_student, student_list)
            all_data = [x for b in all_data for x in b]
            # sql = "INSERT INTO API_studentmarks (subject_name, mark, semester_id, student_id) VALUES "
            # val = ", ".join(all_data[:5000])
            # with closing(connection.cursor()) as cursor:
            #     cursor.execute(f'{sql}{val}')
            print('done')
