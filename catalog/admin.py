from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language

# Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model = Book

#definimos la clase admin para autor
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',  'date_of_birth', 'date_of_death')
    inlines = [BookInline]
#registramos la clase admin con el modelo asociado
admin.site.register(Author, AuthorAdmin)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display= ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('status', 'due_back')
        }),
    )