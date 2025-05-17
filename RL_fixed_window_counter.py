import time
import unittest
from threading import Thread


ONE_SECOND = 1


class FixedWindowCounter:
    def __init__(self, rate_per_sec: int = 1):
        self.rate_per_sec = rate_per_sec
        self.current_volume = 0

        self.th = Thread(target=self.auto_cleaning, name="auto_cleaning_tb", daemon=True)
        print("SYSTEM: Init rate_per_sec=%s" % (rate_per_sec,))
        self.th_stop = False
        print("SYSTEM: Starting autocleaning daemon")
        self.th.start()

    def close(self):
        self.th_stop = True
        self.th.join()

    def clean(self):
        self.current_volume = 0

    def get(self, name: str = "") -> bool:
        if self.current_volume < self.rate_per_sec:
            self.current_volume += 1
            print("SYSTEM: Return token to:", name)
            return True

        return False

    def auto_cleaning(self):
        print("SYSTEM: Autocleaning daemon started")
        while not self.th_stop:
            time.sleep(ONE_SECOND)
            self.clean()
        print("SYSTEM: Autocleaning daemon stopped")


class TestFixedWindowCounter(unittest.TestCase):
    def setUp(self):
        self.tb = FixedWindowCounter(rate_per_sec=10)

    def tearDown(self):
        self.tb.close()

    def test_full_volume(self):
        for i in range(10):
            self.assertTrue(self.tb.get(str(i)))

        for i in range(2):
            self.assertFalse(self.tb.get(str(i)))

    def test_waiting(self):
        self.tb.clean()
        time.sleep(ONE_SECOND)
        for i in range(10):
            self.assertTrue(self.tb.get(str(i)))


if __name__ == "__main__":
    print("Token bucket example")

    unittest.main()

