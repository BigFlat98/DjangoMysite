#템플릿 필터 정의. templatetags -> 폴더명을 지켜줘야 함
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter #템플릿 필터 안에 우리가 정의한 함수를 추가하겠다.
def sub(value, arg):
    return value - arg


@register.filter
def mark(value):
    extensions=["nl2br","fenced_code"] 
    return mark_safe(markdown.markdown(value,extensions=extensions))