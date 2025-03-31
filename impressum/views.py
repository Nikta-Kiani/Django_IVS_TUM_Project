from django.shortcuts import render

# Create your views here.
def impressum_view(request):
    return render(request, 'impressum/impressum.html')