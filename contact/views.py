from django.shortcuts import render, redirect, HttpResponse
from .forms import ContactForm

  
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
          
        if form.is_valid():
            return redirect('http://127.0.0.1:8000/login/')
        else:
            return HttpResponse("Bots are not allowed to use this website!!!")
            
    else:
        form = ContactForm()
          
    return render(request, 'contact.html', {'form':form})