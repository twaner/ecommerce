__author__ = 'taiowawaner'
import string
import random
import uuid

from .models import Order


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    the_id ="".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(id=the_id)
    except Order.DoesNotExist:
        return the_id
    # return "".join(random.choice(chars) for x in range(size))


def uuid_str_generator():
    return str(uuid.uuid4()).upper().replace('-','')[0:20]