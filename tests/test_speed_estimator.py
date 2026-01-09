import pytest
from src.speed_estimator import SpeedEstimator


class TestSpeedEstimator:

    @pytest.fixture
    def estimator(self):
        return SpeedEstimator(
            pixels_per_meter=10.0,
            fps=10,
            frame_height=1000
        )

    def test_no_points_returns_zero(self, estimator):
        speed = estimator.estimate_speed([])
        assert speed == 0.0

    def test_single_point_returns_zero(self, estimator):
        speed = estimator.estimate_speed([(100, 100)])
        assert speed == 0.0

    def test_stationary_vehicle_returns_zero(self, estimator):
        track_points = [(200, 400)] * 10
        speed = estimator.estimate_speed(track_points)
        assert speed == 0.0

    def test_moving_vehicle_speed_positive(self, estimator):
        track_points = [(i * 10, 500) for i in range(10)]
        speed = estimator.estimate_speed(track_points)
        assert speed > 0.0

    def test_speed_is_physically_clamped(self, estimator):
        track_points = [(i * 100, 100) for i in range(10)]
        speed = estimator.estimate_speed(track_points)
        assert speed <= 120.0

    def test_small_jitter_is_ignored(self, estimator):
        track_points = [
            (100, 500),
            (101, 500),
            (100, 501),
            (101, 501),
            (100, 500)
        ]
        speed = estimator.estimate_speed(track_points)
        assert speed == 0.0

    def test_add_vehicle_speed_filters_low_values(self, estimator):
        estimator.add_vehicle_speed(track_id=1, speed=1.5)
        estimator.add_vehicle_speed(track_id=1, speed=10.0)

        avg_speed = estimator.get_average_speed(1)
        assert avg_speed == 10.0

    def test_average_speed_computation(self, estimator):
        estimator.add_vehicle_speed(1, 20.0)
        estimator.add_vehicle_speed(1, 30.0)
        estimator.add_vehicle_speed(1, 40.0)

        avg = estimator.get_average_speed(1)
        assert avg == 30.0

    def test_speed_summary_generation(self, estimator):
        estimator.add_vehicle_speed(1, 20.0)
        estimator.add_vehicle_speed(1, 30.0)
        estimator.add_vehicle_speed(2, 50.0)

        vehicle_type_map = {
            1: "car",
            2: "truck"
        }

        summary = estimator.compute_speed_summary(vehicle_type_map)

        assert "car" in summary
        assert "truck" in summary
        assert summary["car"]["average_speed"] == 25.0
        assert summary["truck"]["average_speed"] == 50.0
