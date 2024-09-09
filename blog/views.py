from django.db.models import Count
from django.shortcuts import render, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .models import Post_djb
from .forms import EmailPostForm, CommentForm, SearchForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.

def post_search(request):
    """
    This view is used to search blog posts using a search form. The view
    will filter the published posts using the search query and rank them
    using the SearchRank function from the django.contrib.postgres.search
    module. The view will then render the results in a template that
    displays the search form and the search results.

    :param request: The request object
    :return: The rendered template
    """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body', config='english')
            search_query = SearchQuery(query)
            results = (
                Post_djb.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query)
                )
                .filter(search=search_query)
                .order_by('-rank')
            )

    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        },
    )

@require_POST
def post_comment(request, post_id):
    """
    Handles the comment submission for a blog post. The view will
    validate the comment form and save the comment if the form is
    valid. The view will then render the comment template to display
    the comment.

    :param request: The request object
    :param post_id: The ID of the post to add the comment to
    :return: The rendered template
    """
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
    tag = None

    def get_queryset(self):        
        queryset = super().get_queryset()
        if self.tag:
            queryset = queryset.filter(tags__in=[self.tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

    def get(self, request, tag_slug=None):
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
        return super().get(request)
    
    
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
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post_djb.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


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
    
