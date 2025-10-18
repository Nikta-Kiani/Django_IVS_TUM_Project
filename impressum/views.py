from django.shortcuts import render

# Create your views here.
def imprint_view(request):
    return render(request, 'imprint/imprint.html')