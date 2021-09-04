from frontpager_framework.frontpager_server import Application
from test_fronts import fronts
from frontpager_framework.frontpager_templator import render

application = Application(fronts)

# page controller
@application.add_route("/")
def index_view(request):
    print(request)
    return render("./templates/authors.html", object_list=[{'name': 'Leo'}, {'name': 'Kate'}])

@application.add_route("/names/")
def abc_view(request):
    print(request)
    if request["method"] == "GET":
        return render("./templates/names.html", object_list=[{'name': 'User'}])
    elif request["method"] == "POST":
        print(request["post"]['name'].value)
        print(request["post"]['password'].value)
        print(request["post"]['email'].value)
        return render("./templates/names.html", object_list=[{'name': request["post"]['name'].value}])


class Other:

    @application.add_route("/othernames/")
    def __call__(self, request):
        print(request)
        return render("./templates/othernames.html", object_list=[{'name': 'meo'}, {'name': 'keo'}])

print(application.routes)