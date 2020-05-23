from xflask import render_template
from xflask.web import route
from xflask.web.controller import Controller


class IndexController(Controller):

    @route('/')
    def index(self):
        return render_template('index.html')
