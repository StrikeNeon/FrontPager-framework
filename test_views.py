from frontpager_framework.frontpager_templator import render


# page controller
def index_view(request):
    print(request)
    return render("./templates/authors.html", object_list=[{'name': 'Leo'}, {'name': 'Kate'}])


def abc_view(request):
    print(request)
    if request["method"] == "GET":
        return render("./templates/names.html", object_list=[{'name': 'User'}])
    elif request["method"] == "POST":
        return render("./templates/names.html", object_list=[request["post"]['name']])

class Other:

    def __call__(self, request):
        print(request)
        return render("./templates/othernames.html", object_list=[{'name': 'meo'}, {'name': 'keo'}])


routes = {
    '/': index_view,
    '/names/': abc_view,
    '/othernames/': Other()
}
