from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.


class Task(models.Model):
    # One-to-many relationship.
    # When a user is deleted, all his items are also deleted.
    # Nulls are possible.
    # Forms may be blank.
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Field for the title. A title may be empty.
    title = models.CharField(max_length=200)
    
    # A text field for the description of the task.
    description = models.TextField(null=True, blank=True)
    
    #A datePicker to mark the date and time.
    date = models.DateTimeField()

    # Checkbox to mark an item as completed.
    complete = models.BooleanField(default=False)
    
    # Automatically take the date and time at the moment of creation a new item.
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'