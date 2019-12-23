import numpy as np
from django.shortcuts import render

from API.models import StudentDetails, SemesterDetails, StudentMarks


def format_student_filter(student_filter):
    _id = int(student_filter.split(',student-')[0].split('(')[1])
    std_id = student_filter.split(',student-')[1].split(')')[0]
    return _id, f"student-{std_id}"


def format_sem_details_filter(year_filter):
    try:
        return eval(year_filter)
    except NameError:
        return 'ALL', 'ALL', 'ALL'


def results(request):
    student_obj = list(StudentDetails.objects.values_list('id', 'student_name'))
    semester_obj = list(
        SemesterDetails.objects.values_list('id', 'calendar_year', 'semester'))
    marks_obj = list(
        StudentMarks.objects.values_list('subject_name', flat=True).distinct())

    semester_obj.insert(0, ('ALL', 'ALL', 'ALL'))
    # marks_obj.insert(0, ('ALL'))

    current_student, *_ = student_obj
    current_semester, *_ = semester_obj
    current_subject, *_ = marks_obj

    bloxpot_req = {
        'student_id': current_student[0]
    }
    if not current_semester[0] == 'ALL':
        bloxpot_req['semester_id'] = current_semester[0]

    if not current_subject == 'ALL':
        bloxpot_req['subject_name'] = current_subject

    data = [
        [760, 801, 848, 895, 965],
        [733, 853, 939, 980, 1080],
        [714, 762, 817, 870, 918],
        [724, 802, 806, 871, 950],
        [834, 836, 864, 882, 910]
    ]
    context = {
        'boxplot': {
            'data': data,
            'minWidth': len(data) * 110,
            'categories': ['sem_2_sub_24568',
                           'sem_2_sub_24568',
                           'sem_2_sub_24568']
        },
        'column': {
            'marks_data': [100],
            'average_data': [50],
            'subjects': ['subject_one']
        },
        'student_details': student_obj,
        'semester_details': semester_obj,
        'subject_details': marks_obj[:5],
    }

    if request.method == 'POST':
        student_filter = request.POST.get('student_filter')
        _format_student_filter = format_student_filter(student_filter)
        year_filter = request.POST.get('year_filter')
        _format_semester_details_filter = format_sem_details_filter(year_filter)
        subject_filter = request.POST.get('subject_filter')

        context['student_details_filter'] = _format_student_filter
        context['semester_details_filter'] = _format_semester_details_filter
        context['subject_details_filter'] = subject_filter

        if not _format_semester_details_filter[0] == 'ALL':
            bloxpot_req['semester_id'] = _format_semester_details_filter[0]

        if not subject_filter == 'ALL':
            bloxpot_req['subject_name'] = subject_filter

    bloxpot_obj = StudentMarks.objects.filter(**bloxpot_req).values_list(
        'subject_name', 'mark')
    bloxpot_dict = {}
    bloxpot_marks = []
    for subject_name, mark in bloxpot_obj:
        if subject_name not in bloxpot_dict.keys():
            bloxpot_dict[subject_name] = []
        bloxpot_dict[subject_name].append(mark)

    for marks in bloxpot_dict.values():
        bloxpot_marks.append(list(np.percentile(marks, [0, 25, 50, 75, 100])))

    boxplot = {
        'data': bloxpot_marks,
        'minWidth': len(bloxpot_marks) * 110,
        'categories': list(bloxpot_dict.keys())
    }
    context['boxplot'] = boxplot

    marks_value = list(bloxpot_dict.values())[0]
    column = {
        'marks_data': [marks_value[0]],
        'average_data': [sum(marks_value) / len(marks_value)],
        'subjects': list(bloxpot_dict.keys())
    }
    context['column'] = column

    return render(request, 'demo/index.html', context=context)
