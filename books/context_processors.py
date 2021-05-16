from .models import Genre

def menu_genre(request):
    genres = Genre.objects.all()

    return ({'genres': genres})
