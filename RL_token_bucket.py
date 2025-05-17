import time
import unittest
from threading import Thread


ONE_SECOND = 1


class TokenBucket:
    def __init__(self, volume: int = 10, rate_per_sec: int = 1):
        self.volume = volume
        self.rate_per_sec = rate_per_sec
        self.current_volume = volume

        self.th = Thread(target=self.auto_increase, name="auto_increase_tb", daemon=True)
        print("SYSTEM: Init volume=%s, rate_per_sec=%s" % (volume, rate_per_sec))
        self.th_stop = False
        print("SYSTEM: Starting autoincrement tokens daemon")
        self.th.start()

    def close(self):
        self.th_stop = True
        self.th.join()

    def clean(self):
        self.current_volume = 0

    def get(self, name: str = "") -> bool:
        if self.current_volume > 0:
            self.current_volume -= 1
            print("SYSTEM: Return token to:", name)
            return True

        return False

    def auto_increase(self):
        print("SYSTEM: Autoincrement tokens daemon started")
        while not self.th_stop:
            time.sleep(ONE_SECOND)
            self.current_volume = min(self.current_volume + self.rate_per_sec, self.volume)
            print("SYSTEM: Added tokens")
        print("SYSTEM: Autoincrement tokens daemon stopped")


class TestTokenBucket(unittest.TestCase):
    def setUp(self):
        self.tb = TokenBucket(volume=10, rate_per_sec=1)

    def tearDown(self):
        self.tb.close()

    def test_full_volume(self):
        for i in range(10):
            self.assertTrue(self.tb.get(str(i)))

        for i in range(2):
            self.assertFalse(self.tb.get(str(i)))

    def test_waiting(self):
        self.tb.clean()
        time.sleep(ONE_SECOND + 0.1)
        self.assertTrue(self.tb.get("11"))
        self.assertFalse(self.tb.get("12"))

class TestTokenBucket(unittest.TestCase):
    def setUp(self):
        self.tb = TokenBucket(volume=2, rate_per_sec=2)

    def tearDown(self):
        self.tb.close()

    def test_overflow(self):
        self.assertTrue(self.tb.get("1"))
        time.sleep(ONE_SECOND + 0.1)
        self.assertTrue(self.tb.get("2"))
        self.assertTrue(self.tb.get("3"))
        self.assertFalse(self.tb.get("4"))

if __name__ == "__main__":
    print("Token bucket example")

    unittest.main()

