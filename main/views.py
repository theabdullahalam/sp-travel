from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, PostType
from django.templatetags.static import static
 
def index(request):
    header_image = static('img/mountains.jpg')
    posts = [
        {
            'header_image': static('/img/ladakh.jpg'),
            'title': 'Dont miss this cool Image!',
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam?'
        },
        {
            'header_image': static('/img/cats.jpg'),
            'title': 'Dont miss this cool Image!',
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam? Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia!'
        },
        {
            'header_image': static('/img/monkey.jpg'),
            'title': 'Dont miss this cool Image!',
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam?'
        }
    ]


    sections = [
        {
            'name': 'Latest Posts',
            'posts': posts
        },

        {
            'name': 'Guides',
            'posts': posts
        }
    ]


    context = {
        'header_image': header_image,
        'sections': sections
    }


    return render(request, 'index.html', context=context)
 
def post(request, slug):
    # FETCH OBJ
    post_obj=Post.objects.get(slug = str(slug))
 
    # HUMAN FRIENDLY DATE
    hfr_date = post_obj.created.strftime('%e %b %Y')
    post_obj.hfr_date = hfr_date
 
    # CREATE CONTEXT
    context = {
        'post': post_obj,
    }
 
    # RETURN
    return render(request, 'post.html', context=context)
 
def posts(request, pageno=1):
    # FETCH ALL POSTS
    # posts = Post.objects.filter(p_type__type_name = typename).exclude(slug='about').order_by('-created', 'title')
    posts = Post.objects.all().order_by('-created', 'title')
 
    # PAGINATE
    paginator = Paginator(posts, 10)
    page_num = int(pageno)
    page_obj = paginator.get_page(page_num)
    posts = page_obj.object_list
 
    # HUMAN FRIENDLY DATE
    for post in posts:
        hfr_date = post.created.strftime('%e %b %Y')
        post.hfr_date = hfr_date
 
        post.preview = str(post.content).split('</p>')[0].split('<p>')[1]
 
    # SET CONTEXT
    context = {
        'posts': posts,
        'pageinator': paginator,
        'page_obj': page_obj,
    }
 
    # RETURN
    return render(request, 'posts.html', context=context)