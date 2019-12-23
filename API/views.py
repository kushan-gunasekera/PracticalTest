from django.shortcuts import get_object_or_404, render


def results(request):
    return render(request, 'demo/index.html')
