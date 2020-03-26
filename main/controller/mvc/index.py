from xflask import render_template
from xflask.classy import route
from xflask.controller import Controller


class IndexController(Controller):

    @route('/')
    def index(self):
        return render_template('index.html')


