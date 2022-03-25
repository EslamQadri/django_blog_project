from django.contrib.syndication.views import Feed 
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post
class LatestPostsFeed(Feed):
    title='My Blog'
    link=reverse_lazy('blog:post_list')
    desciption='NEW Posts of My blog .'
    def items(self):
        return Post.published.all()[:5]
    
    def item_titles(self,item):
        return item.title
    def item_description(self,item):
        return truncatewords(item.body,30)


