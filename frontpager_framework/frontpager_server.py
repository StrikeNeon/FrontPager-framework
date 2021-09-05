from wsgiref.util import setup_testing_defaults
from cgi import FieldStorage
from .generic_views import not_found_404_view, server_error_500_view

#  TODO get post delete etc methods


class Application:

    def __init__(self, fronts, routes={}):
        self.routes = routes
        self.fronts = fronts

    def add_route(self, path):
        def wrapper(func):
            if hasattr(func, '__call__'):
                self.routes[path] = func
            else:
                raise AttributeError(f"{func} view is not callable")
        return wrapper

    def get(self, view, request):
        response_body = view(request)
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        return status, headers, response_body

    def post(self, view, request):
        print(request)
        try:
            response_body = view(request)
        except Exception as ex:
            print(ex)
            response_body = server_error_500_view(request)
            status = '500 error'
            headers = [('Content-type', 'text/plain'),
                       ('Content-Length', str(len(response_body)))]
            return status, headers, response_body
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        return status, headers, response_body

    def serve(self, environ, start_response):
        setup_testing_defaults(environ)
        print('work')
        path = environ['PATH_INFO']
        if path[-1] != '/':
            path += '/'
        method = environ['REQUEST_METHOD']
        request = {}
        request["path"] = path
        request["method"] = method
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view(request)
        # front controller
        for front in self.fronts:
            front(request)
        if method == "GET":
            print(view)
            status, headers, response_body = self.get(view, request)
        elif method == "POST":
            try:
                request_body_size = int(environ['CONTENT_LENGTH'])
            except (TypeError, ValueError):
                request_body_size = 0
            request["size"] = request_body_size
            request["post"] = FieldStorage(fp=environ['wsgi.input'],
                                           environ=environ,
                                           keep_blank_values=True)
            status, headers, response_body = self.post(view, request)
        start_response(status, headers)
        return [bytes(response_body, encoding='utf-8')]

    def __call__(self, environ=None, start_response=None):
        if not environ:
            return
        return self.serve(environ, start_response)
