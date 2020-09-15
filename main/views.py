from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, Page, Author, Category, Place, Comment
from django.templatetags.static import static
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.sites.models import Site

import os

def get_paragraph_preview(content):
    preview = ''

    try:
        first_para = str(content).split('</p>')[0].split('<p>')[1]
        first_twenty = first_para.split(' ')[:20]
        # remove comma from last
        if first_twenty[-1][-1] == ',':
            first_twenty[-1] = first_twenty[-1][:-1]

        preview = '{}...'.format(' '.join(first_twenty), '...')
    except IndexError as ie:
        print(str(ie))
        preview = content

    return preview

def get_protocol():
    if os.environ.get('DEBUG').lower() == 'true':
        return 'http'
    else:
        return 'https'

def get_full_url(ending):
    return '%s://%s%s' % (get_protocol(), Site.objects.get_current().domain, ending)
    
 
def about(request):
    about_page = Page.objects.get(page_name='about')
    authors = Author.objects.all()
    
    context = {
        'header_image': about_page.header_image.url,
        'social_image': get_full_url(about_page.header_image.url),
        'ogurl': get_full_url(reverse('about')),
        'pretitle': about_page.pre_title,
        'title': about_page.title,
        'description': about_page.description,
        'content': about_page.content,
        'authors': authors
    }

    return render(request, 'about.html', context=context)

def index(request):
    index_page = Page.objects.get(page_name='index')

    sections = []

    categories = Category.objects.all()
    for category in categories:
        # GET TOP 4 POSTS UNDER CATEGORT
        posts = Post.objects.filter(category__id = category.id).order_by('-views', 'title').filter(published=True)[:3]

        # SET DATE AND PREVIEW
        for post in posts:
            hfr_date = post.created.strftime('%e %b %Y')
            post.hfr_date = hfr_date

            post.preview = get_paragraph_preview(post.content)

            

        # CREATE SECTION DICT
        section = {
            'name': category.name,
            'posts': posts,
            'category_slug': category.slug
        }


        sections.append(section)

    context = {
        'header_image': index_page.header_image.url,
        'social_image': get_full_url(index_page.header_image.url),
        'ogurl': get_full_url(reverse('index')),
        'pretitle': index_page.pre_title,
        'title': index_page.title,
        'description': index_page.description,
        'sections': sections,
        'categories': categories
    }


    return render(request, 'index.html', context=context)
 
def post(request, slug):

    # FETCH OBJ
    post_obj=Post.objects.get(slug = str(slug))

    # ADD COMMENT IF REQUEST IS POST
    print("The method is ", request.method)
    if request.method == 'POST':
        # FETCH COMMENT INFO
        comment_content = str(request.POST['comment_area'])
        username = str(request.POST['name_input'])

        comment = Comment(content=comment_content, username=username, post=post_obj)
        comment.save()

        # REDIRECT TO POST AGAIN BUT TO THE COMMENTS LIST
        redirecturl = reverse('post', args=(slug,)) + '#comment-section'
        return redirect(redirecturl)


    # fetch comments
    comments = Comment.objects.filter(post__id=post_obj.id).order_by('-created').filter(published=True)
    for comment in comments:
        hfr_date = comment.created.strftime('%e %b %Y')
        comment.hfr_date = hfr_date
 
    # HUMAN FRIENDLY DATE FOR POST
    hfr_date = post_obj.created.strftime('%e %b %Y')
    post_obj.hfr_date = hfr_date

    # POST PREVIEW FOR SCHEMA
    post_obj.preview = get_paragraph_preview(post_obj.content)

    # CATEGORY OF THE POST
    category = Category.objects.get(id=post_obj.category.id)

    # OGTYPE BASED ON CATEGORY
    ogtype = 'article'
    if category.name == 'Blog':
        ogtype = 'blog'


    # AUTHORS OF THE POST
    authors = post_obj.authors.all()

    # INCREMENT POST VIEWS
    post_obj.views = int(post_obj.views) + 1
    post_obj.save()




    # THREE RELATED POSTS
    related_posts = []
    forbidden_ids = [post_obj.id]

    # LISTS OF POSTS TO USE
    category_posts = Post.objects.filter(category__id = post_obj.category.id)
    place_posts = Post.objects.filter(place__id = post_obj.place.id)

    # FIRST RELATED POST
    post1 = None
    most_viewed = category_posts.order_by('views')
    index = 0
    try:
        while True:
            post1 = most_viewed[index]

            if post1.id in forbidden_ids:
                index += 1
            else:
                related_posts.append(post1)
                forbidden_ids.append(post1.id)
                break
    except IndexError:
        pass   

    # SECOND RELATED POST IS A RANDOM POST FROM SAME CATEGORY
    post2 = None
    latest = category_posts.order_by('-created')
    index = 0
    try:
        while True:
            post2 = latest[index]

            if post2.id in forbidden_ids:
                index += 1
            else:
                related_posts.append(post2)
                forbidden_ids.append(post2.id)
                break
    except IndexError:
        pass

    # THIRD RELATED POST IS RANDOM POST FROM SAME PLACE
    post3 = None
    latest = place_posts.order_by('-created')
    index = 0
    try:
        while True:
            post3 = latest[index]

            if post3.id in forbidden_ids:
                index += 1
            else:
                related_posts.append(post3)
                forbidden_ids.append(post3.id)
                break
    except IndexError:
        pass
     
    # CREATE CONTEXT
    context = {
        'header_image': post_obj.header_image.url,
        'social_image': get_full_url(post_obj.header_image.url),
        'ogurl': get_full_url(reverse('post', args=[slug])),
        'ogtype': ogtype,
        'full_logo_url': get_full_url(static('img/logo.png')),
        'category': category,
        'authors': authors,
        'post': post_obj,
        'comments': comments,
        'related_posts': related_posts
    }
 
    # RETURN
    return render(request, 'post.html', context=context)
 
def posts(request, section='all', slug='none', pageno=1):
    posts = []
    section_name = ''

    # FETCH INDEX PAGE FOR HEADER IMAGE
    index_page = Page.objects.get(page_name='index')
    header_image = index_page.header_image.url

    
    if section == 'category':
        posts = Post.objects.filter(category__slug = slug).order_by('-created', 'title').filter(published=True)
        category = Category.objects.get(slug=slug)
        section_name = str(category.name).title()
        header_image = category.header_image.url

    elif section == 'place':
        posts = Post.objects.filter(place__slug = slug).order_by('-created', 'title').filter(published=True)
        place = Place.objects.get(slug=slug)
        section_name = str(place.name).title()
        header_image = place.header_image.url

    else:
        posts = Post.objects.all().order_by('-created', 'title').filter(published=True)
        section_name = 'All'
 
    # PAGINATE
    paginator = Paginator(posts, 10)
    page_num = int(pageno)
    page_obj = paginator.get_page(page_num)
    posts = page_obj.object_list
 
    # HUMAN FRIENDLY DATE
    # AND PREVIEW PARA
    for post in posts:
        hfr_date = post.created.strftime('%e %b %Y')
        post.hfr_date = hfr_date
 
        post.preview = get_paragraph_preview(post.content)

    # CATEGORY LIST FOR HEADER
    categories = Category.objects.all()
 
    # SET CONTEXT
    context = {
        'header_image': header_image,
        'social_image': get_full_url(header_image),
        'ogurl': get_full_url(reverse('posts', args=[section, slug, pageno])),
        'description': index_page.description,
        'section': section_name,
        'posts': posts,
        'pageinator': paginator,
        'page_obj': page_obj,
        'categories': categories
    }   
    
 
    # RETURN
    return render(request, 'posts.html', context=context)



def places(request, pageno=1):

    place_page = Page.objects.get(page_name='places')

    # ALL PLACES
    places = Place.objects.all()

    # PAGINATE
    paginator = Paginator(places, 10)
    page_num = int(pageno)
    page_obj = paginator.get_page(page_num)
    places = page_obj.object_list

    # CATEGORY LIST FOR HEADER
    categories = Category.objects.all()

    context = {
        'header_image': place_page.header_image.url,
        'social_image': get_full_url(place_page.header_image.url),
        'ogurl': get_full_url(reverse('places', args=[pageno])),
        'description': place_page.description,
        'pretitle': place_page.pre_title,
        'bigtitle': place_page.title,
        'places': places,
        'pageinator': paginator,
        'page_obj': page_obj,
        'categories': categories
    }   
    
 
    # RETURN
    return render(request, 'places.html', context=context)





def privacy(request):

    privacy_page = Page.objects.get(page_name='privacy')

    # CATEGORY LIST FOR HEADER
    categories = Category.objects.all()

    context = {
        'header_image': privacy_page.header_image.url,
        'social_image': get_full_url(privacy_page.header_image.url),
        'ogurl': get_full_url(reverse('privacy')),
        'description': privacy_page.description,
        'pretitle': privacy_page.pre_title,
        'bigtitle': privacy_page.title,
        'content': privacy_page.content,
        'categories': categories
    }   
    
 
    # RETURN
    return render(request, 'privacy.html', context=context)


