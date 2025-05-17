import time
import unittest
from threading import Thread


ONE_SECOND = 1


class LeakyBucket:
    def __init__(self, volume: int = 10, rate_per_sec: int = 1):
        self.volume = volume
        self.rate_per_sec = rate_per_sec
        self.current_volume = volume
        self.queue = []

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

    def get_status(self, name: str = "") -> str:
        if name in self.queue:
            if name == self.queue[0]:
                return "ready"
            return "wait"

        elif len(self.queue) < self.volume:
            self.queue.append(name)
            if len(self.queue) <= self.rate_per_sec:
                return "ready"

            return "wait"

        return "reject"

    def auto_increase(self):
        print("SYSTEM: Autoincrement tokens daemon started")

        while not self.th_stop:
            time.sleep(ONE_SECOND)
            decrease_amount = self.rate_per_sec
            while len(self.queue) > 0 and decrease_amount > 0:
                decrease_amount -= 1
                name = self.queue.pop(0)
                print("SYSTEM: Remove ready token for: ", name)

        print("SYSTEM: Autoincrement tokens daemon stopped")


class TestLeakyBucket(unittest.TestCase):
    def setUp(self):
        self.tb = LeakyBucket(volume=5, rate_per_sec=1)

    def tearDown(self):
        self.tb.close()

    def test_full_volume(self):
        self.assertEqual(self.tb.get_status("1"), "ready")
        self.assertEqual(self.tb.get_status("2"), "wait")
        self.assertEqual(self.tb.get_status("3"), "wait")
        self.assertEqual(self.tb.get_status("4"), "wait")
        self.assertEqual(self.tb.get_status("5"), "wait")
        self.assertEqual(self.tb.get_status("6"), "reject")

        time.sleep(1.1)
        self.assertEqual(self.tb.get_status("2"), "ready")
        self.assertEqual(self.tb.get_status("3"), "wait")
        self.assertEqual(self.tb.get_status("4"), "wait")
        self.assertEqual(self.tb.get_status("5"), "wait")
        self.assertEqual(self.tb.get_status("6"), "wait")
        self.assertEqual(self.tb.get_status("1"), "reject")


if __name__ == "__main__":
    print("Token bucket example")

    unittest.main()

