from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, Page, Author, Category, Place
from django.templatetags.static import static
 
def about(request):
    about_page = Page.objects.get(page_name='about')
    authors = Author.objects.all()
    
    context = {
        'header_image': about_page.header_image.url,
        'pretitle': about_page.pre_title,
        'title': about_page.title,
        'description': about_page.description,
        'content': about_page.content,
        'authors': authors
    }

    return render(request, 'about.html', context=context)

def index(request):
    index_page = Page.objects.get(page_name='index')

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
        'header_image': index_page.header_image.url,
        'pretitle': index_page.pre_title,
        'title': index_page.title,
        'description': index_page.description,
        'sections': sections
    }


    return render(request, 'index.html', context=context)
 
def post(request, slug):
    # FETCH OBJ
    post_obj=Post.objects.get(slug = str(slug))
    # post_obj = {
    #         'header_image': static('/img/ladakh.jpg'),
    #         'title': 'Dont miss this extra super cool Image!',
    #         'preview': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quae eligendi sapiente vel minima ex cumque qui esse eos mollitia veniam?',
    #         'content': '''<p>
    #                     Lorem ipsum dolor sit, amet consectetur adipisicing elit. Similique cumque, impedit quos libero ducimus deserunt repellat, unde pariatur nostrum ratione non minus sit neque aspernatur consequatur eveniet! Animi, veniam consectetur!
    #                 </p>
    #                 <p>
    #                     Lorem, ipsum dolor sit amet consectetur adipisicing elit. Dolorem dolor ducimus porro iure aperiam consectetur libero necessitatibus magni quae nesciunt doloremque eveniet hic sit commodi quas enim rerum, sequi dolores id adipisci nostrum, aspernatur fuga est error? Corporis harum velit laudantium atque error id commodi, a numquam dolorem minima accusamus vel laborum voluptate magnam enim nihil adipisci deleniti eos et?
    #                 </p>
    #                 <img data-src="/static/img/cats.jpg" class="lozad" />
    #                 <div class="caption"><small><em>Cool Cats</em></small></div>
    #                 <p>
    #                     Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio, architecto eaque asperiores saepe, nihil nisi, optio laborum blanditiis maxime impedit unde. Cum minus fugiat iure odio incidunt officiis magnam, nisi doloremque cupiditate laboriosam quod necessitatibus earum ut ducimus repellat repudiandae ipsa quo nulla quos. Deserunt architecto earum voluptas, fugiat magnam explicabo saepe? Minus iusto modi cum ab nesciunt sit dolorem adipisci nemo molestiae est. Ea saepe assumenda sit eveniet reprehenderit fugit aliquam dolor dolore dignissimos ratione, fugiat sunt earum corporis! Facilis, minus temporibus iste ex deserunt vel molestias, consequatur tempora ad eaque distinctio. Enim ipsam dolorem, error ad natus, iusto atque dignissimos voluptatum, cupiditate autem alias! Ducimus voluptates, rerum culpa porro accusantium modi incidunt, dolor deleniti placeat laborum, maiores dolorem.
    #                 </p>
    #                 <p>
    #                     Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus repellendus nobis fugiat. Delectus doloribus et aut quis nesciunt officiis optio sit ducimus illo similique repellendus consectetur exercitationem quos cupiditate impedit voluptate tempora quo facere voluptas dolorum, dignissimos laudantium earum? Animi porro incidunt, vero asperiores amet reiciendis illo voluptatem nesciunt iusto repudiandae autem corrupti! In, mollitia!
    #                 </p>''',
    #         'slug': 'dummy-post',
    # }

    comment = {
        'body': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Expedita, in quae exercitationem vel nostrum eius. Ipsa iure ab eaque, dicta animi quam, ducimus officiis eos voluptatibus odio reiciendis laudantium autem?',
        'display_name': 'some_rando',
        'date': '30th August 2020'
    }

    comments = []

    for i in range(0,7):
        comments.append(comment)
 
    # HUMAN FRIENDLY DATE
    hfr_date = post_obj.created.strftime('%e %b %Y')
    post_obj.hfr_date = hfr_date

    # CATEGORIES OF THE POST
    categories = post_obj.categories.all()

    # AUTHORS OF THE POST
    authors = post_obj.authors.all()
 
    # CREATE CONTEXT
    context = {
        'header_image': post_obj.header_image.url,
        'categories': categories,
        'authors': authors,
        'post': post_obj,
        'comments': comments
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
        posts = Post.objects.filter(categories__slug = slug).order_by('-created', 'title')
        category = Category.objects.get(slug=slug)
        section_name = str(category.name).title()
        header_image = category.header_image.url

    elif section == 'place':
        posts = Post.objects.filter(place__slug = slug).order_by('-created', 'title')
        place = Place.objects.get(slug=slug)
        section_name = str(place.name).title()
        header_image = place.header_image.url

    else:
        posts = Post.objects.all().order_by('-created', 'title')
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
 
        post.preview = str(post.content).split('</p>')[0].split('<p>')[1]
 
    # SET CONTEXT
    context = {
        'header_image': header_image,
        'description': index_page.description,
        'section': section_name,
        'posts': posts,
        'pageinator': paginator,
        'page_obj': page_obj,
    }
 
    # RETURN
    return render(request, 'posts.html', context=context)