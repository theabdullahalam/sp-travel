from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.contrib.sites.models import Site


# PLACE MODEL FOR PLACES IN THE BLOG
class Place(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    header_image = models.ImageField(upload_to='place_headers')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs): 
        # GENERATE SLUG
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Place, self).save(*args, **kwargs)
 
    def __str__(self):
        return str(self.name)
 
    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

# FOR INDIVIDUAL PAGES
class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    header_image = models.ImageField(upload_to='page_headers')
    page_name = models.CharField(max_length=200)
    pre_title = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=600)
    content = RichTextUploadingField(max_length=14000)



# AUTHORS
class Author(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    display_picture = models.ImageField(upload_to='author_images')
    name = models.CharField(max_length=75)
    bio = models.TextField(max_length=700, default='A short description')

# GUIDE, BLOG, PHOTOGRAPHY
class Category(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    header_image = models.ImageField(upload_to='category_headers')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs): 
        # GENERATE SLUG
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)
 
    def __str__(self):
        return str(self.name)
 
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
 
class Post(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    header_image = models.ImageField(upload_to='post_headers')
    title = models.CharField(max_length=250)
    # p_type=models.ForeignKey(PostType, on_delete=models.CASCADE)
    content = RichTextUploadingField(max_length=14000)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    views = models.IntegerField(editable=False, default=0)
    published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
 
    def save(self, *args, **kwargs):
        # UPDATE TIMESTAMPS
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
 
        # GENERATE SLUG
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
 
    def __str__(self):
        return str(self.title)
 
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    content = models.TextField(max_length=2000)
    username = models.CharField(max_length=100)
    created = models.DateTimeField(editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # UPDATE TIMESTAMPS
        if not self.id:
            self.created = timezone.now()

        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.content[:30] + '...')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'