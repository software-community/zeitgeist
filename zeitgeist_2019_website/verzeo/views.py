from django.shortcuts import render

# Create your views here.

def verzeo_home(request):
    return render(request, 'verzeo/index.html')


def arts_commerce(request):
    return render(request, 'verzeo/arts&commerce.html')


def bio(request):
    return render(request, 'verzeo/bio.html')

def nano(request):
    return render(request, 'verzeo/bio/nano.html')


def civil(request):
    return render(request, 'verzeo/civil.html')


def cse(request):
    return render(request, 'verzeo/cse.html')


def ece(request):
    return render(request, 'verzeo/ece.html')


def management(request):
    return render(request, 'verzeo/management.html')


def mech(request):
    return render(request, 'verzeo/mech.html')
