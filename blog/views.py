from django.shortcuts import render, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post_djb
from .forms import EmailPostForm, CommentForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST
# Create your views here.

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post_djb, id=post_id, status=Post_djb.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post_djb,
        id=post_id,
        status=Post_djb.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        },
    )
    
