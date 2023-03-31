from django.core.paginator import Paginator


def make_pagination(request, posts):
    posts_per_page = 10
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}
