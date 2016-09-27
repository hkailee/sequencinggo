from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from event.models import Conference
from .cart import Cart
from .forms import CartAddConferenceForm


@require_POST
def cart_add(request, conference_id):
    cart = Cart(request)
    conference = get_object_or_404(Conference, id=conference_id)
    form = CartAddConferenceForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(conference=conference,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, conference_id):
    cart = Cart(request)
    conference = get_object_or_404(Conference, id=conference_id)
    cart.remove(conference)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddConferenceForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
