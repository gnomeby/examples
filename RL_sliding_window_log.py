import time
import unittest


ONE_SECOND = 1


class SlidingWindowLog:
    def __init__(self, rate_per_sec: int = 1):
        self.rate_per_sec = rate_per_sec
        self.ts = []

        print("SYSTEM: Init rate_per_sec=%s" % (rate_per_sec,))

    def get(self, name: str = "") -> bool:
        # Autocleanup
        while self.ts and (time.time() - self.ts[0]) > ONE_SECOND:
            self.ts.pop(0)

        if len(self.ts) < self.rate_per_sec:
            self.ts.append(time.time())
            print("SYSTEM: Return token to:", name)
            return True

        return False


class TestSlidingWindowLog(unittest.TestCase):
    def setUp(self):
        self.tb = SlidingWindowLog(rate_per_sec=5)

    def test_full_volume(self):
        for i in range(5):
            self.assertTrue(self.tb.get(str(i)))

        for i in range(5):
            self.assertFalse(self.tb.get(str(i)))

    def test_waiting(self):
        self.assertTrue(self.tb.get("first"))
        time.sleep(ONE_SECOND/100)

        for i in range(4):
            self.assertTrue(self.tb.get(str(i)))

        time.sleep(ONE_SECOND-ONE_SECOND/100)

        self.assertTrue(self.tb.get("6"))
        self.assertFalse(self.tb.get("7"))


if __name__ == "__main__":
    print("Sliding Window Log example")

    unittest.main()
