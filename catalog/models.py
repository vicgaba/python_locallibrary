from django.db import models

# Create your models here.

class Genre(models.Model):
    ''' Modelo para el género del libro '''
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género")

    def __str__(self):
        return self.name

from django.urls import reverse #usado para generar el URL reverso 
class Book(models.Model):
    '''Modelo para representar el libro'''

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Seleccione un género para este libro")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        '''Creamos el texto para géneros'''
        return ', '.join([genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description='Género'
    
import uuid #requerida para las instancias de libros únicos

class BookInstance(models.Model):
    '''Representamos cada copia específica del libro'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS=(
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices = LOAN_STATUS, blank=True, default='m', help_text="Disponibilidad del libro")

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('language-books', args=[str(self.id)])
    def __str__(self):
        return self.name