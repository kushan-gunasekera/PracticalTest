from rest_framework import serializers

from .models import SemesterDetails, StudentDetails, StudentMarks


# for view
class StudentDetailsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetails
        fields = ['id', 'student_name']


# for view
class SemesterDetailsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterDetails
        fields = ['id', 'calendar_year']


# for view
class StudentMarksViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMarks
        fields = ['id', 'subject_name']
