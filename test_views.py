from frontpager_framework.frontpager_templator import render


# page controller
def index_view(request):
    print(request)
    return render("./templates/authors.html", object_list=[{'name': 'Leo'}, {'name': 'Kate'}])


def abc_view(request):
    print(request)
    return render("./templates/authors.html", object_list=[{'name': 'a'}, {'name': 'n'}])


class Other:

    def __call__(self, request):
        print(request)
        render("./templates/authors.html", object_list=[{'name': 'meo'}, {'name': 'keo'}])


routes = {
    '/': index_view,
    '/abc/': abc_view,
    '/other/': Other()
}
