from django import template

register = template.Library()


@register.filter
def media_url(image_path):
    if image_path:
        return f'/media/{image_path}'
    return ''
