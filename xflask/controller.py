from xflask.classy.flask_classy import FlaskView

from xflask.component import Component


class Controller(FlaskView, Component):
    route_base = ''
