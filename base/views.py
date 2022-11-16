from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms

from django.contrib.auth.views import LoginView
# LoginRequiredMixin allows us to protect our views from being accessed without a login.
# Let all views that should be protected from unauthorized users inherit from the LoginRequiredMixin class.
# Add the LoginRequiredMixin as the first superclass in the views.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Once the user is registered, he should automatically be loggend in.
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'

    # Show all fields in the form of the imported login view.
    fields = '__all__'
    redirect_authenticated_user = True

    # Once the user is logged in, take him to the list view.
    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # Once the form is valid, the user should be logged in.
    def form_valid(self, form):
        # Get the user
        user = form.save()
        if user is not None:
            # If the user has been successfully created, login him diretly.
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')

        # If the user is not authenticated, the program continues what it is
        # supposed to do.
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass in some context data
        # Make sure that each user can only see his own data
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # Get the search input or an empty string if no search words are provided
        search_input = self.request.GET.get('search-area') or ''
        if search_input:

            # Only show items whose titles start with the given search input 
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class: PositionForm
    # Let the user only see the form fields that he should be able to interact with
    fields = ['title', 'description', 'date' , 'complete']

    # If an item was created successfully, redirect the user to the tasks homepage
    success_url = reverse_lazy('tasks')

    # Separate user accounts from each other
    # Let the user be able to create items for his own account only
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
        
    def get_form(self, form_class=None):

        if form_class is None: 
            form_class = self.form_class
        form = super(TaskCreate, self).get_form(form_class)
        form.fields['date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return form


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'date' , 'complete']
    success_url = reverse_lazy('tasks')

    form_class: PositionForm

    def get_form(self, form_class=None):

        if form_class is None: 
            form_class = self.form_class
        form = super(TaskUpdate, self).get_form(form_class)
        form.fields['date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return form


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

def get_form(self, form_class=None):

        if form_class is None: 
            form_class = self.form_class
        form = super(TaskCreate, self).get_form(form_class)
        form.fields['date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return form