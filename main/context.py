from xflask.context import ApplicationStateListener

class AppContextInitializer(ApplicationStateListener):

    def on_start(self, application):
        pass

    def on_stop(self, application):
        pass
