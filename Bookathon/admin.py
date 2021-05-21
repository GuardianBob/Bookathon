from django.contrib import admin

from loginApp.models import User as U
from Bookathon.models import Book, Author, Review, Genre

class UAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
admin.site.register(U, UAdmin)

class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book, BookAdmin)

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)

class ReviewAdmin(admin.ModelAdmin):
    pass
admin.site.register(Review, ReviewAdmin)

class GenreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Genre, GenreAdmin)
