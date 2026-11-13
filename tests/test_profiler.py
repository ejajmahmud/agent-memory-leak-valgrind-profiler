"""Unit tests for agent-memory-leak-valgrind-profiler."""
import unittest
from agent_memory_leak_valgrind_profiler.profiler import MemoryLeakProfiler

class TestLeakProfiler(unittest.TestCase):
    def setUp(self):
        self.profiler = MemoryLeakProfiler(leak_threshold_bytes=500)

    def test_detect_leak(self):
        self.profiler.start()
        leaked = [bytearray(10000) for _ in range(5)]
        rep = self.profiler.stop_and_evaluate()
        self.assertTrue(rep.is_leaking)
        self.assertGreater(rep.growth_bytes, 1000)

if __name__ == "__main__":
    unittest.main()
