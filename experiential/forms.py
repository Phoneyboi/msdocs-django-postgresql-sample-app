from django import forms
from django.core.exceptions import ValidationError
from .models import LessonLearned, AuthenticImmersiveExperience, Experience, ExperientialFrame

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class LessonLearnedForm(forms.ModelForm):

    experiential_frame = forms.ModelChoiceField(
        queryset=ExperientialFrame.objects.all(),
        required=True,
        label='Experiential Frame',
        empty_label=None
    )
    experience = forms.ModelChoiceField(
        queryset=Experience.objects.all(),  # Empty queryset, will be filled via JavaScript
        required=True,
        label='Experience',
        empty_label=None
    )
    aie_name = forms.ModelChoiceField(
        queryset=AuthenticImmersiveExperience.objects.all(),
        # Empty queryset, will be filled based on Experience selection
        required=True,
        label='Authentic Immersive Experience',
        empty_label=None
    )

    class Meta:
        model = LessonLearned
        fields = ['experiential_frame', 'experience', 'aie_name', 'takeaway', 'learning_statement', 'value_statement']
        labels = {
            'takeaway': 'Takeaway',
            'learning_statement': 'Insight',
            'value_statement': 'Value',
        }

    def __init__(self, *args, **kwargs):
        super(LessonLearnedForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            frame_id = kwargs['initial'].get('experiential_frame')
            experience_id = kwargs['initial'].get('experience')
            aie_id = kwargs['initial'].get('aie_name')

            if frame_id:
                self.fields['experiential_frame'].queryset = ExperientialFrame.objects.filter(id=frame_id)
            if experience_id:
                self.fields['experience'].queryset = Experience.objects.filter(id=experience_id)
            if aie_id:
                self.fields['aie_name'].queryset = AuthenticImmersiveExperience.objects.filter(id=aie_id)

    def clean(self):
        # Call the base class first
        cleaned_data = super().clean()
        # Now check for uniqueness
        if LessonLearned.objects.filter(
                takeaway=cleaned_data.get("takeaway"),
                learning_statement=cleaned_data.get("learning_statement"),
                value_statement=cleaned_data.get("value_statement"),
        ).exists():
            raise ValidationError("Your Takeaway, Insight, and Value must be unique.")
        return cleaned_data

    def clean_learning_statement(self):  # Also known as 'Insight'
        learning_statement = self.cleaned_data.get('learning_statement')
        # Replace 'required_string' with the string you want to enforce
        required_strings = ['I discovered', 'I learned']  # os.getenv('LEARNING_STATEMENT_REQUIRED_STRINGS').split(',')[:]
        if not any(required_string in learning_statement for required_string in required_strings):
            raise ValidationError(f"Must include one of the acceptable strings: {required_strings}")
        return learning_statement

    def clean_value_statement(self):  # Also known as 'Value'
        value_statement = self.cleaned_data.get('value_statement')
        # Replace 'required_string' with the string you want to enforce
        required_strings = ['has value', 'is valuable', 'is important']  # os.getenv('VALUE_STATEMENT_REQUIRED_STRINGS').split(',')[:]
        if not any(required_string in value_statement for required_string in required_strings):
            raise ValidationError(f"Must include one of the acceptable strings: {required_strings}")
        return value_statement
