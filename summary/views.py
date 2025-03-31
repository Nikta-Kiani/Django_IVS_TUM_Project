from django.shortcuts import render

# Create your views here.
def summary_view(request):
    return render(request, 'summary/summary.html')
