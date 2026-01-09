class SpeedEstimator:
    """
    Perspective-aware speed estimator using depth-based scaling.
    """

    def __init__(self, pixels_per_meter, fps, frame_height):
        try:
            self.base_ppm = pixels_per_meter
            self.fps = fps
            self.frame_height = frame_height

            self.vehicle_speed_history = {}

        except Exception as e:
            print(f"Error in SpeedEstimator.__init__: {e}")

    # --------------------------------------------------
    def estimate_speed(self, track_points, window_size=5, noise_threshold=2):
        try:
            if track_points is None or len(track_points) < 2:
                return 0.0

            recent_points = track_points[-window_size:]
            total_meters = 0.0

            for i in range(1, len(recent_points)):
                x1, y1 = recent_points[i - 1]
                x2, y2 = recent_points[i]

                pixel_dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                if pixel_dist < noise_threshold:
                    continue

                # ---------------- DEPTH SCALING (KEY FIX) ----------------
                y_center = (y1 + y2) / 2
                depth_scale = max(0.2, (self.frame_height - y_center) / self.frame_height)

                effective_ppm = self.base_ppm * depth_scale
                meters = pixel_dist / effective_ppm

                total_meters += meters

            time_seconds = (len(recent_points) - 1) / self.fps
            if time_seconds <= 0:
                return 0.0

            speed_kmph = (total_meters / time_seconds) * 3.6

            # ---------------- PHYSICAL CLAMP ----------------
            speed_kmph = min(speed_kmph, 120.0)  # realistic upper bound

            return round(speed_kmph, 2)

        except Exception as e:
            print(f"Error in estimate_speed: {e}")
            return 0.0

    # --------------------------------------------------
    def add_vehicle_speed(self, track_id, speed):
        try:
            if track_id not in self.vehicle_speed_history:
                self.vehicle_speed_history[track_id] = []

            if speed >= 2:
                self.vehicle_speed_history[track_id].append(speed)

        except Exception as e:
            print(f"Error in add_vehicle_speed: {e}")

    # --------------------------------------------------
    def get_average_speed(self, track_id):
        try:
            speeds = self.vehicle_speed_history.get(track_id, [])
            return round(sum(speeds) / len(speeds), 2) if speeds else 0.0
        except Exception as e:
            print(f"Error in get_average_speed: {e}")
            return 0.0

    # --------------------------------------------------
    def compute_speed_summary(self, vehicle_type_map):
        try:
            summary = {}

            for track_id, speeds in self.vehicle_speed_history.items():
                vehicle_type = vehicle_type_map.get(track_id)
                if not speeds or vehicle_type is None:
                    continue

                avg = sum(speeds) / len(speeds)

                if vehicle_type not in summary:
                    summary[vehicle_type] = {"speeds": []}

                summary[vehicle_type]["speeds"].append(avg)

            final = {}
            for v, data in summary.items():
                speeds = data["speeds"]
                final[v] = {
                    "average_speed": round(sum(speeds) / len(speeds), 2),
                    "distribution": self._speed_distribution(speeds)
                }

            return final

        except Exception as e:
            print(f"Error in compute_speed_summary: {e}")
            return {}

    # --------------------------------------------------
    def _speed_distribution(self, speeds):
        ranges = {"0-20": 0, "20-40": 0, "40-60": 0, "60+": 0}
        for s in speeds:
            if s < 20:
                ranges["0-20"] += 1
            elif s < 40:
                ranges["20-40"] += 1
            elif s < 60:
                ranges["40-60"] += 1
            else:
                ranges["60+"] += 1
        return ranges
