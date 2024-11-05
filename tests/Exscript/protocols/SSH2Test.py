from __future__ import absolute_import
import sys
import unittest
import re
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from .ProtocolTest import ProtocolTest
from Exscript.servers import sshd, SSHd
from Exscript.protocols import SSH2
from Exscript import PrivateKey

keyfile = os.path.join(os.path.dirname(__file__), 'id_rsa')
key = PrivateKey.from_file(keyfile)


class SSH2Test(ProtocolTest):
    CORRELATE = SSH2

    def createDaemon(self):
        self.daemon = SSHd(self.hostname, self.port, self.device, key=key)

    def createProtocol(self):
        self.protocol = SSH2(timeout=1)

    def testConstructor(self):
        self.assertIsInstance(self.protocol, SSH2)

    def testGetRemoteVersion(self):
        self.assertEqual(self.protocol.get_remote_version(), None)
        self.doConnect()
        self.assertEqual(self.protocol.get_remote_version(), sshd.local_version)

    def testLogin(self):
        self.assertRaises(IOError, ProtocolTest.testLogin, self)

    def testAuthenticate(self):
        self.assertRaises(IOError, ProtocolTest.testAuthenticate, self)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(SSH2Test)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
