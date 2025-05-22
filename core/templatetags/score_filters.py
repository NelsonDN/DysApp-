from django import template

register = template.Library()

@register.filter
def score_class(score):
    try:
        score = float(score)
    except (ValueError, TypeError):
        return 'bg-danger'
    
    if score < 20:
        return 'bg-danger'
    elif score < 40:
        return 'bg-warning'
    elif score < 60:
        return 'bg-info'
    elif score < 80:
        return 'bg-success'
    else:
        return 'bg-primary'
