from django.db import models


class StudentDetails(models.Model):
    student_id = models.CharField(max_length=10)
    student_name = models.CharField(max_length=50)


class SemesterDetails(models.Model):
    semester = models.PositiveSmallIntegerField()
    grade = models.PositiveSmallIntegerField()
    calendar_year = models.PositiveSmallIntegerField()


class StudentMarks(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    semester = models.ForeignKey(SemesterDetails, on_delete=models.SET_NULL,
                                 null=True)
    subject_name = models.CharField(max_length=15)
    mark = models.PositiveSmallIntegerField()
