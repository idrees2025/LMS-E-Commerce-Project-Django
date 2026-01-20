from django.db.models import F,ExpressionWrapper,FloatField,Avg,Count

ALLOWED_SORT_FIELDS = {
    'created_at':'created_at',
    'popular': 'reviews',
    'new_arrival': '-created_at',
    '-percent_off': '-percent_off',
    'discounted_price':'discounted_price'
}

def apply_sorting(queryset, request, default='created_at'):
    if request.GET.get('sort') == 'discounted_price':
        queryset = queryset.annotate(
            discounted_price=ExpressionWrapper(
                F('price') * (1 - F('percent_off') / 100),
                output_field=FloatField()
            )
        )
    elif request.GET.get('sort') == 'reviews':
        queryset=queryset.annotate(review_avg=Avg('reviews')).order_by('-review_avg')
    sort_by = request.GET.get('sort', default)
    sort_field = ALLOWED_SORT_FIELDS.get(sort_by, ALLOWED_SORT_FIELDS[default])
    return queryset.order_by(sort_field),sort_by
