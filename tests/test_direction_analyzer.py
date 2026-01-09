import unittest
from src.direction_analyzer import DirectionAnalyzer


class TestDirectionAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DirectionAnalyzer(threshold=5)

    def test_in_direction(self):
        # Moving towards BOTTOM of frame
        points = [(200, 250), (200, 300)]
        self.assertEqual(self.analyzer.analyze_direction(points), "IN")

    def test_out_direction(self):
        # Moving towards TOP of frame
        points = [(200, 300), (200, 250)]
        self.assertEqual(self.analyzer.analyze_direction(points), "OUT")

    def test_small_movement(self):
        points = [(200, 300), (200, 302)]
        self.assertEqual(self.analyzer.analyze_direction(points), "UNKNOWN")

    def test_invalid_track(self):
        points = [(200, 300)]
        self.assertEqual(self.analyzer.analyze_direction(points), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
