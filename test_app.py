from frontpager_framework.frontpager_server import Application
from test_fronts import fronts
from test_views import routes

application = Application(routes, fronts)
