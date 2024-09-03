from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post_djb
# Create your views here.

def post_list(request):
    """
    Displays a list of published posts.

    :param request: The request object
    :return: A rendered HTML page
    """
    posts = Post_djb.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    
    """
    Displays a single post.

    :param request: The request object
    :param id: The ID of the post to display
    :return: A rendered HTML page
    """
    post = get_object_or_404(Post_djb, id = id, status = Post_djb.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})