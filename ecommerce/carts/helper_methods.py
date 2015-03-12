__author__ = 'taiowawaner'


def request_get_helper(request, name):
    """
    Returns a tuple of values from a request.
    :param request: request.
    :param name: name of value to get from request.
    :return:
    """
    try:
        val = request.GET.get(name)
        updated = True
    except:
        val = None
        updated = False
    return val, updated
