from django.contrib.sitemaps import Sitemap
from .models import Post_djb

class PostSitemap(Sitemap):
    chagefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post_djb.published.all()
    
    def lastmod(self, obj):
        return obj.updated
    