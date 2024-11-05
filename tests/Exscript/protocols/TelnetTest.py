from __future__ import absolute_import
import sys
import unittest
import re
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from .ProtocolTest import ProtocolTest
from Exscript import Account
from Exscript.servers import Telnetd
from Exscript.protocols import Telnet


class TelnetTest(ProtocolTest):
    CORRELATE = Telnet

    def createDaemon(self):
        self.daemon = Telnetd(self.hostname, self.port, self.device)

    def createProtocol(self):
        self.protocol = Telnet(timeout=1)

    def testConstructor(self):
        self.assertIsInstance(self.protocol, Telnet)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TelnetTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
