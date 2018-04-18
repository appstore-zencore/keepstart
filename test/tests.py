import time
import unittest
import threading
import platform
from keepserver import findvip
from keepserver import call
from keepserver import is_running
from keepserver import server
from keepserver import stop_flag

class TestKeepstart(unittest.TestCase):

    def setUp(self):
        self.nic = "lo"
        if "darwin" == platform.system().lower():
            self.nic = "lo0"
        if "windows" == platform.system().lower():
            self.nic = "Loopback Pseudo-Interface 1"

    def test01(self):
        assert findvip("127.0.0.1") == True
        assert findvip("127.0.0.1", nic=self.nic) == True
        assert findvip("127.0.0.2", nic=self.nic) == False
        assert findvip("127.0.0.1", nic="never-exist") == None

    def test02(self):
        assert call("echo hello")
        assert not call("never-exist")

        if platform.system().lower() in ["linux", "darwin"]:
            assert call("true")
            assert not call("false")

    def test03(self):
        assert is_running(None, True, 100, 3, False) == True
        assert is_running(None, True, 100, 4, True) == True
        assert is_running(None, False, 100, 4, False) == False
        assert is_running(None, False, 100, 4, True) == False
        assert is_running(None, None, 100, 4, False) == False
        assert is_running(None, None, 100, 4, True) == False

        assert is_running("true", None, 100, 4, True) == True
        assert is_running("false", None, 100, 4, True) == False
        assert is_running({"a": 1}, None, 100, 4, True) == None # os.system expect a string param if meet a dict throw TypeError exception.

        assert is_running("true", False, 0, 100, False) == True
        assert is_running("true", False, 1, 100, False) == False
        assert is_running("true", False, 100, 100, False) == True

    def test04(self):
        config = {
            "keepstart": {
                "sleep": 1,
                "vip": "127.0.0.1",
                "start": "echo start04",
                "stop": "echo stop04",
                "running-report-cycle" :10,
                "force-test-cycle": 3,
            }
        }
        t = threading.Thread(target=server, args=[config])
        t.setDaemon(True)
        t.start()
        time.sleep(3)
        stop_flag.set()
        time.sleep(3)

    def test05(self):
        config = {
            "keepstart": {
                "sleep": 1,
                "vip": "127.0.0.2",
                "start": "echo start05",
                "stop": "echo stop05",
                "is-running": "true",
                "running-report-cycle" :10,
                "force-test-cycle": 3,
            }
        }
        t = threading.Thread(target=server, args=[config])
        t.setDaemon(True)
        t.start()
        time.sleep(3)
        stop_flag.set()
        time.sleep(3)
