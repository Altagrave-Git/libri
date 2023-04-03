from django.db import models
from django.urls import reverse
import uuid


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=600, null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField('Genre')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book", kwargs={"pk": self.pk})
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    data_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse("author", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book copy across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status =  models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id}, {self.book.title}'#type:ignore


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


class Language(models.Model):
    
    LANGUAGE_CHOICES = (
        ('en', 'English'), ('af', 'Afrikaans'), ('sq', 'Albanian'), ('ar', 'Arabic'), ('eu', 'Basque'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bs', 'Bosnian'), ('bg', 'Bulgarian'), ('my', 'Burmese'), ('ca', 'Catalan'), ('zh', 'Chinese'), ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'), ('nl', 'Dutch'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('fi', 'Finnish'), ('fr', 'French'), ('gl', 'Galician'), ('de', 'German'), ('el', 'Greek'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('is', 'Icelandic'), ('id', 'Indonesian'), ('it', 'Italian'), ('ja', 'Japanese'), ('kk', 'Kazakh'), ('ko', 'Korean'), ('la', 'Latin'), ('lv', 'Latvian'), ('lt', 'Lithuanian'), ('mk', 'Macedonian'), ('ms', 'Malay'), ('mt', 'Maltese'), ('no', 'Norwegian'), ('fa', 'Persian'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sr', 'Serbian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('es', 'Spanish'), ('sw', 'Swahili'), ('sv', 'Swedish'), ('tl', 'Tagalog'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('uk', 'Ukrainian'), ('vi', 'Vietnamese'), ('cy', 'Welsh')
    )

    lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, blank=True, default='en', help_text='Book language')

    def __str__(self):
        return self.lang