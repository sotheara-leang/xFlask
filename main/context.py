from xflask.component import Component
from xflask.context import ApplicationStateListener

class AppContextInitializer(Component, ApplicationStateListener):

    def on_start(self, application):
        pass

    def on_stop(self, application):
        pass
