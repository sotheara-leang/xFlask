import logging

from xflask.component import Component
from xflask.context import ApplicationStateListener

class AppContextInitializer(Component, ApplicationStateListener):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def on_start(self, application):
        self.logger.debug('START')

    def on_stop(self, application):
        self.logger.debug('STOP')
