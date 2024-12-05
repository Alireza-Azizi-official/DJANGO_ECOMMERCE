from .models import Category

def menu_link(request):
    links = Category.objects.all()
    return dict(link = links)