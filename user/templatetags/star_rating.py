from django import template

register = template.Library()

@register.filter
def fa_star_rating(value):
    if not value and value!=0:
        return 'no rating'

    full_stars = int(value)
    half_star = 1 if (value - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars_html = '<i class="fas fa-star"></i>' * full_stars
    if half_star:
        stars_html += '<i class="fas fa-star-half-alt"></i>'
    stars_html += '<i class="far fa-star"></i>' * empty_stars

    return stars_html
