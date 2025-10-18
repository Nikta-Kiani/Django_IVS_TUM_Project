from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
                        # Check if there is a 'next' parameter in the URL (i.e., a user tried accessing a protected page)
            #next_url = request.GET.get('next')

            # Redirect to 'next' page if available, otherwise go to a default page (e.g., 'antenna')
            #if next_url:
            #    return redirect(next_url)
          #  else:
         #       return redirect('antenna')  # Default page after login
        #else:
       #     messages.error(request, 'Invalid username or password.')
    #else:
        #form = AuthenticationForm()

   # return render(request, 'login/login.html', {'form': form})
            # Redirect to 'next' if available, otherwise go to the antenna page
         #   next_url = request.GET.get('configuration', 'antenna')  # 'antenna' is the fallback if no 'next'
          #  return redirect(next_url)
            return redirect('antenna')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login/login.html')
