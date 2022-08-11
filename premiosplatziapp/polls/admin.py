from dataclasses import fields
from django.contrib import admin
from django.forms import forms

from .models import Question, Choice

class MinTwoChoicesValidation:
    """
    Validates that a minimum of 2 choices have been 
    created for a question before getting saved.
    """
    validate_min = True
    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min, *args, **kwargs)
        

class ChoiceInline(MinTwoChoicesValidation, admin.StackedInline):
    model = Choice
    min_num = 2
    validate_min = True
    extra = 1


class ChoiceAdmin(admin.ModelAdmin):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    fields = ["pub_date", "question_text"]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
