class DirectionAnalyzer:
    """
    Determines vehicle direction (IN / OUT) for a top-down fixed camera
    based on net vertical displacement.
    """

    def __init__(self, threshold=10):
        """
        Args:
            threshold (int): minimum pixel movement to consider valid direction
        """
        try:
            self.threshold = threshold
        except Exception as e:
            print(f"Error in DirectionAnalyzer.__init__: {e}")

    # --------------------------------------------------
    # SINGLE TRACK DIRECTION
    # --------------------------------------------------
    def analyze_direction(self, track_points):
        """
        Args:
            track_points (list): list of (x, y) tuples

        Returns:
            str: 'IN', 'OUT', or 'UNKNOWN'
        """
        try:
            if track_points is None or len(track_points) < 2:
                return "UNKNOWN"

            start_y = track_points[0][1]
            end_y = track_points[-1][1]

            displacement = end_y - start_y

            # Ignore very small movements
            if abs(displacement) < self.threshold:
                return "UNKNOWN"

            # Moving towards BOTTOM of frame → IN
            if displacement > 0:
                return "IN"

            # Moving towards TOP of frame → OUT
            return "OUT"

        except Exception as e:
            print(f"Error in analyze_direction: {e}")
            return "UNKNOWN"

    # --------------------------------------------------
    # ALL TRACKS
    # --------------------------------------------------
    def analyze_all_tracks(self, track_history):
        """
        Args:
            track_history (dict):
                { track_id: [(x1, y1), (x2, y2), ...] }

        Returns:
            dict:
                { track_id: 'IN' / 'OUT' / 'UNKNOWN' }
        """
        try:
            directions = {}

            for track_id, points in track_history.items():
                directions[track_id] = self.analyze_direction(points)

            return directions

        except Exception as e:
            print(f"Error in analyze_all_tracks: {e}")
            return {}
