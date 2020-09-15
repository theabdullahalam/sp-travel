from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Place

class PostSiteMap(Sitemap):
    changefreq = "monthly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.modified


class CategorySiteMap(Sitemap):
    changefreq = "monthly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Category.objects.all()

class PlaceSiteMap(Sitemap):
    changefreq = "monthly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Place.objects.all()