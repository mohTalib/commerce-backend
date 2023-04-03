from django.contrib import admin
from .models import User, category, listing, Comment, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(listing)
admin.site.register(category)
admin.site.register(Comment)
admin.site.register(Bid)
