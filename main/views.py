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
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam?',
            'slug': 'dummy-post'
        },
        {
            'header_image': static('/img/cats.jpg'),
            'title': 'Dont miss this cool Image!',
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam? Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia!',
            'slug': 'dummy-post'
        },
        {
            'header_image': static('/img/monkey.jpg'),
            'title': 'Dont miss this cool Image!',
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam?',
            'slug': 'dummy-post'
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
    # post_obj=Post.objects.get(slug = str(slug))
    post_obj = {
            'header_image': static('/img/ladakh.jpg'),
            'title': 'Dont miss this extra super cool Image!',
            'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam?',
            'content': '''<p>
    Lorem ipsum dolor sit, amet consectetur adipisicing elit. Similique cumque, impedit quos libero ducimus deserunt repellat, unde pariatur nostrum ratione non minus sit neque aspernatur consequatur eveniet! Animi, veniam consectetur!
</p>
<p>
    Lorem, ipsum dolor sit amet consectetur adipisicing elit. Dolorem dolor ducimus porro iure aperiam consectetur libero necessitatibus magni quae nesciunt doloremque eveniet hic sit commodi quas enim rerum, sequi dolores id adipisci nostrum, aspernatur fuga est error? Corporis harum velit laudantium atque error id commodi, a numquam dolorem minima accusamus vel laborum voluptate magnam enim nihil adipisci deleniti eos et?
</p>
<img data-src="/static/img/cats.jpg" class="lozad" />
<div class="caption"><small><em>Cool Cats</em></small></div>
<p>
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio, architecto eaque asperiores saepe, nihil nisi, optio laborum blanditiis maxime impedit unde. Cum minus fugiat iure odio incidunt officiis magnam, nisi doloremque cupiditate laboriosam quod necessitatibus earum ut ducimus repellat repudiandae ipsa quo nulla quos. Deserunt architecto earum voluptas, fugiat magnam explicabo saepe? Minus iusto modi cum ab nesciunt sit dolorem adipisci nemo molestiae est. Ea saepe assumenda sit eveniet reprehenderit fugit aliquam dolor dolore dignissimos ratione, fugiat sunt earum corporis! Facilis, minus temporibus iste ex deserunt vel molestias, consequatur tempora ad eaque distinctio. Enim ipsam dolorem, error ad natus, iusto atque dignissimos voluptatum, cupiditate autem alias! Ducimus voluptates, rerum culpa porro accusantium modi incidunt, dolor deleniti placeat laborum, maiores dolorem.
</p>
<p>
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus repellendus nobis fugiat. Delectus doloribus et aut quis nesciunt officiis optio sit ducimus illo similique repellendus consectetur exercitationem quos cupiditate impedit voluptate tempora quo facere voluptas dolorum, dignissimos laudantium earum? Animi porro incidunt, vero asperiores amet reiciendis illo voluptatem nesciunt iusto repudiandae autem corrupti! In, mollitia!
</p>''',
            'slug': 'dummy-post',
    }

    comment = {
        'body': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Expedita, in quae exercitationem vel nostrum eius. Ipsa iure ab eaque, dicta animi quam, ducimus officiis eos voluptatibus odio reiciendis laudantium autem?',
        'display_name': 'some_rando',
        'date': '30th August 2020'
    }

    comments = []

    for i in range(0,7):
        comments.append(comment)
 
    # HUMAN FRIENDLY DATE
    # hfr_date = post_obj.created.strftime('%e %b %Y')
    # post_obj.hfr_date = hfr_date

    print(comments)
 
    # CREATE CONTEXT
    context = {
        'header_image': post_obj['header_image'],
        'post': post_obj,
        'comments': comments
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