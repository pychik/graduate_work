from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')

    ordering = ('name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры'


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork
    # raw_id_fields = ['person']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):

    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating',)

    list_filter = ('type', 'genres')

    search_fields = ('title', 'description', 'id')

    ordering = ('title',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    ordering = ('full_name',)
