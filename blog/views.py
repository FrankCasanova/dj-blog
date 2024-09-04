from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post_djb
from django.views.generic import ListView
# Create your views here.

class PostListView(ListView):
    queryset = Post_djb.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'
    


# def post_list(request):

#     """
#     Displays a list of posts.

#     :param request: The request object
#     :return: A rendered HTML page
#     """
#     post_list = Post_djb.published.all()
#     paginator = Paginator(post_list, 4)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)  
#     return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    
    """
    Displays a single post.

    :param request: The request object
    :param id: The ID of the post to display
    :return: A rendered HTML page
    """
    post = get_object_or_404(
        Post_djb,
        status = Post_djb.Status.PUBLISHED,
        slug = post,
        publish__year = year,
        publish__month = month,
        publish__day = day
        )
    return render(request, 'blog/post/detail.html', {'post': post})