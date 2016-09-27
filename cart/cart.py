from decimal import Decimal
from django.conf import settings
from event.models import Conference


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the conferences from the database.
        """
        conference_ids = self.cart.keys()
        # get the conference objects and add them to the cart
        conferences = Conference.objects.filter(id__in=conference_ids)
        for conference in conferences:
            self.cart[str(conference.id)]['conference'] = conference

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, conference, quantity=1, update_quantity=False):
        """
        Add a conference to the cart or update its quantity.
        """
        conference_id = str(conference.id)
        if conference_id not in self.cart:
            self.cart[conference_id] = {'quantity': 0,
                                      'price': str(conference.price)}
        if update_quantity:
            self.cart[conference_id]['quantity'] = quantity
        else:
            self.cart[conference_id]['quantity'] += quantity
        self.save()

    def remove(self, conference):
        """
        Remove a conference from the cart.
        """
        conference_id = str(conference.id)
        if conference_id in self.cart:
            del self.cart[conference_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
