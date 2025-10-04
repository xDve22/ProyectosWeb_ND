from django import template
from datetime import datetime, timezone

register = template.Library()

@register.filter
def short_timesince(value):
    if not value:
        return ""
    now = datetime.now(timezone.utc)
    diff = now - value

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    weeks = days // 7
    months = days // 30
    years = days // 365

    if years >= 1:
        return f"{int(years)}y ago"
    elif months >= 1:
        return f"{int(months)}m ago"
    elif weeks >= 1:
        return f"{int(weeks)}w ago"
    elif days >= 1:
        return f"{int(days)}d ago"
    elif hours >= 1:
        return f"{int(hours)}h ago"
    elif minutes >= 1:
        return f"{int(minutes)}m ago"
    else:
        return "just now"
