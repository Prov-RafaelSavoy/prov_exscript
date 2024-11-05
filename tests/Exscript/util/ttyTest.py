from builtins import int
import sys
import unittest
import re
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import tempfile
from subprocess import Popen, PIPE
import Exscript.util.tty


class ttyTest(unittest.TestCase):
    CORRELATE = Exscript.util.tty

    def setUp(self):
        self.tempfile = tempfile.TemporaryFile()
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.stdin = sys.stdin
        sys.stdout = sys.stderr = sys.stdin = self.tempfile

    def _unredirect(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        sys.stdin = self.stdin

    def tearDown(self):
        self._unredirect()
        self.tempfile.close()

    def testGetTerminalSize(self):
        from Exscript.util.tty import get_terminal_size

        # This hack really makes the test incomplete because
        # get_terminal_size() won't be able to check the cterm size,
        # but it is the only way to test at least partially.
        os.ctermid = lambda: '/nosuchfileexists'

        # By deleting PATH we prevent get_terminal_size() from asking
        # the stty unix program.
        oldpath = os.environ['PATH']
        os.environ['PATH'] = ''

        # If the LINES and COLUMNS variables are not set, all methods should
        # now fail, and the default values are returned.
        os.environ['LINES'] = ''
        os.environ['COLUMNS'] = ''
        self.assertEqual(get_terminal_size(), (25, 80))
        self.assertEqual(get_terminal_size(10, 10), (10, 10))

        # If the LINES and COLUMNS variables are set, they should be used.
        os.environ['LINES'] = '1111'
        os.environ['COLUMNS'] = '1111'
        self.assertEqual(get_terminal_size(), (1111, 1111))
        self.assertEqual(get_terminal_size(10, 10), (1111, 1111))

        # If the stty program exists, it should be used.
        os.environ['PATH'] = oldpath
        try:
            # Unfortunately, the 'stty' program on travis actually returns
            # (1111, 1111) if the LINES and COLUMNS env variables are set,
            # so there is no way to tests whether stty was used or the env
            # vars.
            #self.assertNotEqual(get_terminal_size(), (1111, 1111))
            self.assertNotEqual(get_terminal_size(10, 10), (25, 80))
        except OSError:
            pass  # "stty" not found.

        # Lastly, if stdin/stderr/stdout exist, they should tell us something.
        os.environ['PATH'] = ''
        self._unredirect()
        # Same travis problem as above...
        #self.assertNotEqual(get_terminal_size(), (1111, 1111))
        #self.assertNotEqual(get_terminal_size(10, 10), (1111, 1111))
        self.assertNotEqual(get_terminal_size(10, 10), (25, 80))
        os.environ['PATH'] = oldpath


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ttyTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
