from django import template

register = template.Library()

@register.simple_tag
def urlReplace(request, field, value):
    urlDict = request.GET.copy()
    urlDict[field] = value
    return urlDict.urlencode()
