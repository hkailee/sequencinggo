from django.shortcuts import render, get_object_or_404
from .models import Category, Conference
from cart.forms import CartAddConferenceForm


def conference_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    conferences = Conference.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        conferences = conferences.filter(category=category)
    return render(request, 'event/conference/list.html', {'category': category,
                                                      'categories': categories,
                                                      'conferences': conferences})


def conference_detail(request, id, slug):
    conference = get_object_or_404(Conference, id=id, slug=slug, available=True)
    cart_conference_form = CartAddConferenceForm()
    return render(request,
                  'event/conference/smds_detail.html',
                  {'conference': conference,
                   'cart_conference_form': cart_conference_form})


def smds_detail(request, id, slug):
    conference = get_object_or_404(Conference, id=id, slug=slug, available=True)
    return render(request, 'event/conference/smds_detail.html',)