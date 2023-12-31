# In your_app/templatetags/your_app_extras.py

from django import template

register = template.Library()

@register.filter(name='is_textarea')
def is_textarea(field):
    return field.field.widget.__class__.__name__ == 'Textarea'

# In experiential_extras.py

@register.filter
def is_select(field):
    return field.field.widget.__class__.__name__ in ['Select', 'SelectMultiple']
