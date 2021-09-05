from frontpager_framework.frontpager_server import AppFactory

app = AppFactory.create_app()

# page controller
@app.add_route("/")
def index_view(request):
    print(request)
    return app.render_template("./templates/authors.html", object_list=[{'name': 'Leo'}, {'name': 'Kate'}])

@app.add_route("/names/")
def abc_view(request):
    print(request)
    if request["method"] == "GET":
        return app.render_template("./templates/names.html", object_list=[{'name': 'User'}])
    elif request["method"] == "POST":
        print(request["post"]['name'].value)
        print(request["post"]['password'].value)
        print(request["post"]['email'].value)
        return app.render_template("./templates/names.html", object_list=[{'name': request["post"]['name'].value}])


class Other:

    @app.add_route("/othernames/")
    def __call__(self, request):
        print(request)
        return app.render_template("./templates/othernames.html", object_list=[{'name': 'meo'}, {'name': 'keo'}])


# Front controllers
@app.add_front()
def secret_front(request):
    request['secret'] = 'some secret'

@app.add_front()
def other_front(request):
    request['key'] = 'key'
