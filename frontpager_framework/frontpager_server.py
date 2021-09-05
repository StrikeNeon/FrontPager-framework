import abc
from wsgiref.util import setup_testing_defaults
from cgi import FieldStorage
import json
from jinja2 import Environment, FileSystemLoader
from frontpager_framework.frontpager_templator import render
from .generic_views import not_found_404_view, server_error_500_view

#  TODO get post delete etc methods


class AbstractApplication(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, view, request):
        pass

    @abc.abstractmethod
    def post(self, view, request):
        pass

    @abc.abstractmethod
    def put(self, view, request):
        pass

    @abc.abstractmethod
    def patch(self, view, request):
        pass

    @abc.abstractmethod
    def delete(self, view, request):
        pass

    @abc.abstractmethod
    def serve(self, environ, start_response):
        pass

    @abc.abstractmethod
    def render_template(self, template_name, **kwargs):
        pass

    @abc.abstractmethod
    def __call__(self, environ=None, start_response=None):
        pass


class Html_Response:
    def __init__(self, template_path, **kwargs):
        self.path = template_path
        self.template_variables = kwargs

    def __call__(self):
        return render(self.path, self.template_variables)


class Json_Response:
    def __init__(self, data):
        self.data = data

    def __call__(self):
        return json.dumps(self.data)


class ConcreteApplication(AbstractApplication):

    def __init__(self, fronts=[], routes={}, template_path="templates/"):
        self.routes = routes
        self.fronts = fronts
        self.jinja_env = Environment(loader=FileSystemLoader(template_path))

    def add_route(self, path):
        def wrapper(func):
            self.routes[path] = func
        return wrapper

    def add_front(self):
        def wrapper(func):
            self.fronts.append(func)
        return wrapper

    def get(self, view, request):
        response_body = view(request)
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        return status, headers, response_body

    def patch(self, view, request):
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

    def put(self, view, request):
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

    def delete(self, view, request):
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
        elif method == "PATCH":
            try:
                request_body_size = int(environ['CONTENT_LENGTH'])
            except (TypeError, ValueError):
                request_body_size = 0
            request["size"] = request_body_size
            request["post"] = FieldStorage(fp=environ['wsgi.input'],
                                           environ=environ,
                                           keep_blank_values=True)
            status, headers, response_body = self.patch(view, request)
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
        elif method == "PUT":
            try:
                request_body_size = int(environ['CONTENT_LENGTH'])
            except (TypeError, ValueError):
                request_body_size = 0
            request["size"] = request_body_size
            request["post"] = FieldStorage(fp=environ['wsgi.input'],
                                           environ=environ,
                                           keep_blank_values=True)
            status, headers, response_body = self.put(view, request)
        elif method == "DELETE":
            try:
                request_body_size = int(environ['CONTENT_LENGTH'])
            except (TypeError, ValueError):
                request_body_size = 0
            request["size"] = request_body_size
            request["post"] = FieldStorage(fp=environ['wsgi.input'],
                                           environ=environ,
                                           keep_blank_values=True)
            status, headers, response_body = self.delete(view, request)
        start_response(status, headers)
        return [bytes(response_body, encoding='utf-8')]

    def render_template(self, template_name, **kwargs):
        """
        Минимальный пример работы с шаблонизатором
        :param template_name: имя шаблона
        :param kwargs: параметры для передачи в шаблон
        :return:
        """
        # Открываем шаблон по имени
        with open(template_name, encoding='utf-8') as f:
            # Читаем
            template_str = f.read()
        html_string = self.jinja_env.from_string(template_str)
        return html_string.render(default_start_page_lanes=html_string,
                                  **kwargs)

    def __call__(self, environ=None, start_response=None):
        if not environ:
            return
        return self.serve(environ, start_response)


class AppFactory:
    @staticmethod
    def create_app(fronts=[], routes={}, template_path="templates/"):
        app = ConcreteApplication(fronts, routes, template_path)
        return app
