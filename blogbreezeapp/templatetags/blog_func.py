from django import template
from django.utils.timezone import now
from datetime import timedelta

register = template.Library()

@register.filter
def dayssince(value):
    if not value:
        return ""
    delta = now() - value
    days = delta.days
    if days == 0:
        return "today"
    elif days == 1:
        return "yesterday"
    else:
        return f"{days} days ago"