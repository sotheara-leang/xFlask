from test.test_case import TestCase
from xflask.common.util.shell_util import *


class TestUserDao(TestCase):

    def test_run_cmd(self):
        result = run_cmd('pwd')
        print('>>>', result)

    def test_run_cmd_open(self):
        result = run_cmd_popen('./sample1.sh').read()
        print('>>> ', result)

