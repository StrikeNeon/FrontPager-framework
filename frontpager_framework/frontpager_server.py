from wsgiref.util import setup_testing_defaults
from .generic_views import not_found_404_view, server_error_500_view

#  TODO get post delete etc methods


class Application:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def get(self, view, request):
        response_body = view(request)
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        return status, headers, response_body

    def post(self, view, request):
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

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        print('work')
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view()
        request = {}
        request["path"] = path
        # front controller
        for front in self.fronts:
            front(request)
        if method == "GET":
            status, headers, response_body = self.get(view, request)
        elif method == "POST":
            try:
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size)
            except (TypeError, ValueError):
                request_body_size = 0
                request_body = "0"
            request["size"] = request_body_size
            request["body"] = request_body
            status, headers, response_body = self.post(view, request)
        start_response(status, headers)
        return [bytes(response_body, encoding='utf-8')]
