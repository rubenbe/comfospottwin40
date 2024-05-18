import unittest
import comfospot40

from pathlib import Path


class TestStateLoad(unittest.TestCase):
    def test_empty_file(self):
        state = comfospot40.State(60, False)
        state_default = comfospot40.State(60, False)
        hal = comfospot40.Hal(state, 60)
        with open(
            Path(__file__).parent / "state_store_test/empty.json", "r"
        ) as storefile:
            hal.loadState(storefile, state)
        self.assertEqual(state, state_default)

    def test_broken_file(self):
        state = comfospot40.State(60, False)
        state_default = comfospot40.State(60, False)
        hal = comfospot40.Hal(state, 60)
        with open(
            Path(__file__).parent / "state_store_test/broken.json", "r"
        ) as storefile:
            hal.loadState(storefile, state)
        self.assertEqual(state, state_default)

    def test_v2_file(self):
        state = comfospot40.State(60, False)
        state_default = comfospot40.State(60, False)
        hal = comfospot40.Hal(state, 60)
        with open(Path(__file__).parent / "state_store_test/v2.json", "r") as storefile:
            hal.loadState(storefile, state)
        self.assertEqual(state, state_default)
