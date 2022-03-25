from tkinter import NONE
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .form import EmailPostForm, CommentForm,SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector

# Create your views here.


def post_shere(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # from was submitted
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # print(cd['to'])
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # print(post_url)
            subject = f"{cd['name']} recommends you read "f"{post.title}"
            # print(subject)
            message = f"Read {post.title} at {post_url} \n\n" f"{cd['name']} \'s comments : {cd['comments']}"
            # print(message)
            send_mail(subject, message, 'ekadryahmed@gamil.com', [cd['to']])
            sent = True

            # ....send email
    else:
        form = EmailPostForm()


    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})

'''
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
'''


def post_list(request,tag_slug=None):

    objects_list=Post.published.all()
    tag=None
    if tag_slug:
        tag= get_object_or_404(Tag,slug=tag_slug)
        objects_list=Post.published.filter(tags__in=[tag])

    paginator=Paginator(objects_list,3) #3 posts in each page
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #if page is not an ainteger deliver the frist page
        posts=paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver the last page of results
        posts=Paginator.page(paginator.num_pages)
    
    return render(request,'blog/post/list.html',{'posts': posts,'page':page,'tag':tag})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # save the comment to database
            new_comment.save()

        else:
            comment_form = CommentForm()
    

    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
     'comments':comments,'new_comment': new_comment, 'comment_form': comment_form,'similar_posts':similar_posts})

def post_search(request):
    form = SearchForm() 
    query = None
    results = []
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body')).filter(search=query)
        
    return render(request,'blog/post/search.html',{'form':form,'query':query,'results':results})
