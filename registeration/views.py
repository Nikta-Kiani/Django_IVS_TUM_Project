from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegisterationForm
from django.contrib import messages

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = RegisterationForm()
        messages.error(request, 'Please correct the errors below.')
    return render(request, 'registeration/registeration.html', {'form': form})