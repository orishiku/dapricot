from django.shortcuts import render

def error_400(request, exception=None):
    data = {}
    return render(request,'dapricot/error_400.html', data)

def error_403(request, exception=None):
    data = {}
    return render(request,'dapricot/error_403.html', data)

def error_404(request, exception=None):
    data = {}
    return render(request,'dapricot/error_404.html', data)

def error_500(request, exception=None):
    data = {}
    return render(request,'dapricot/error_500.html', data)