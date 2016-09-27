from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.context_processors import csrf

from taggit.models import Tag
from haystack.query import SearchQuerySet

from .forms import PostCreateForm, EmailPostForm, CommentForm, SearchForm
from .models import Post, Comment
from common.decorators import ajax_required
from actions.utils import create_action
import redis

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required
def post_create(request):
    """
    View for creating a new post.
    """
    if request.method == 'POST':
        # form is sent
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            tags = form.cleaned_data['tags']
            new_item.save()
            for tag in tags:
                new_item.tags.add(tag)
            new_item.save()
            create_action(request.user, 'created a post:', new_item)
            messages.success(request, 'Post added successfully')
            form = PostCreateForm()
        else:
            messages.error(request, 'Error adding new post')

    else:
        # build form 
        form = PostCreateForm(data=request.GET)

    return render(request, 'posts/post/create.html', {'section': 'posts',
                                                        'form': form})
                                                        
                                                        
               
                                                    
def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    # increment total post views by 1
    total_views = r.incr('post:{}:views'.format(post.id))
    # increment post ranking by 1
    r.zincrby('post_ranking', post.id, 1)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # assign current user to the item
            new_comment.user = request.user
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            try: 
                postID = Post.objects.get(id=id)
                create_action(request.user, 'created a comment on', postID)
            except:
                pass
            messages.success(request, 'Comment added successfully')
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-created')[:4]
    return render(request, 'posts/post/detail.html', {'sections': 'posts',
    												 'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     'total_views': total_views})



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@sequencingthefuture.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'posts/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
        return render(request, 'posts/post/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results})
    return render(request, 'posts/post/search.html', {'form': form,})



@ajax_required
@login_required
@require_POST
def post_vote(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'vote':
                post.users_like.add(request.user)
                create_action(request.user, 'voted', post)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})


@login_required
def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    for post in posts:
    	post.total_views = r.get('post:{}:views'.format(post.id))

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'posts/post/list_ajax.html',
                      {'section': 'posts', 
                      'page': page, 
                      'posts': posts, 
                      'tag': tag})
    return render(request,
                  'posts/post/list.html',
                   {'section': 'posts', 
                   'page': page, 
                   'posts': posts, 
                   'tag': tag})



def post_list_by_tag(request, tag_slug=None):
    posts = Post.objects.all()    	
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        for post in posts:
            post.total_views = r.get('post:{}:views'.format(post.id))

    paginator = Paginator(posts, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        if request.is_ajax():
            return HttpResponse('')    	
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
    	return render(request, 'posts/post/list_ajax.html', {'page': page,
                                                   			'posts': posts,
                                                   			'tag': tag})
    return render(request, 'posts/post/list_by_tag.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts/post/list.html'




@login_required
def post_mostviewed(request):
    # get post ranking dictionary
    post_ranking = r.zrange('post_ranking', 0, -1, desc=True)[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    # get most viewed posts
    most_viewed = list(Post.objects.filter(id__in=post_ranking_ids))
    most_viewed.sort(key=lambda x: post_ranking_ids.index(x.id))
    for post in most_viewed:
    	post.total_views = r.get('post:{}:views'.format(post.id))

    return render(request,
                  'posts/post/mostviewed.html',
                  {'section': 'posts',
                   'most_viewed': most_viewed})



@login_required
def mypost(request):
    myPost = list(Post.objects.filter(user=request.user))
    for post in myPost:
    	post.total_views = r.get('post:{}:views'.format(post.id))
    
    paginator = Paginator(myPost, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        myPost = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        myPost = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        myPost = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'posts/post/list_ajax_mypost.html',
                      {'section': 'posts', 
                      'page': page, 
                      'mypost': myPost,})
    return render(request,
                  'posts/post/mypost.html',
                   {'section': 'posts', 
                   'page': page, 
                   'mypost': myPost,})
                   
@login_required
def post_remove(request, post_id):
    Post.objects.filter(id=post_id).delete()
    return redirect('posts:mypost')

@login_required
def post_edit(request, post_id):
    item = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('posts:mypost')

    else:
        form = PostCreateForm(instance=item)

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('posts/post/post_edit.html', args)