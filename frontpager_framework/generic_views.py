def not_found_404_view(request):
    print(request)
    return [b'404 PAGE Not Found']


def forbidden_403_view(request):
    print(request)
    return [b'403 FROBIDDEN']


def server_error_500_view(request):
    print(request)
    return [b'500 SERVER ERROR']