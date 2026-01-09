import cv2
from ultralytics import YOLO


class DetectorTracker:
    """
    Handles vehicle detection, tracking, and counting
    using YOLOv8 + BoT-SORT.
    Vehicles are considered only when fully visible
    inside the frame (border filtering applied).
    """

    def __init__(self, model_path="yolov8l.pt", confidence_threshold=0.4):
        try:
            self.model_path = model_path
            self.confidence_threshold = confidence_threshold

            self.model = None
            self.seen_ids = set()

            self.vehicle_counts = {
                "car": 0,
                "bike": 0,
                "bus": 0,
                "truck": 0
            }

            # track_id -> list of (cx, cy)
            self.track_history = {}

            self.load_model()

        except Exception as e:
            print(f"Error in DetectorTracker.__init__: {e}")

    # --------------------------------------------------
    # MODEL LOADING
    # --------------------------------------------------
    def load_model(self):
        try:
            self.model = YOLO(self.model_path)
        except Exception as e:
            print(f"Error in load_model: {e}")

    # --------------------------------------------------
    # FRAME PROCESSING
    # --------------------------------------------------
    def process_frame(self, frame, frame_index):
        """
        Runs detection + tracking on a single frame.
        Vehicles near frame borders are ignored to ensure
        full visibility before counting and tracking.

        Returns:
            List of dictionaries containing:
            track_id, vehicle_type, bbox, center, frame
        """
        try:
            tracked_objects = []

            frame_height, frame_width, _ = frame.shape
            margin = 30  # pixels (border safety margin)

            results = self.model.track(
                frame,
                conf=self.confidence_threshold,
                persist=True,
                tracker="botsort.yaml",
                verbose=False
            )

            if not results or results[0].boxes is None:
                return tracked_objects

            boxes = results[0].boxes

            for box in boxes:
                if box.id is None:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # --------------------------------------------------
                # BORDER FILTERING (KEY FIX)
                # --------------------------------------------------
                # Ignore vehicles that are not fully inside frame
                if (
                    x1 < margin or
                    y1 < margin or
                    x2 > frame_width - margin or
                    y2 > frame_height - margin
                ):
                    continue

                track_id = int(box.id.item())
                class_id = int(box.cls.item())

                vehicle_type = self.map_class(class_id)
                if vehicle_type is None:
                    continue

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Update counts ONLY after full visibility
                self.update_counts(track_id, vehicle_type)

                # Update track history ONLY after full visibility
                self.update_track_history(track_id, (cx, cy))

                tracked_objects.append({
                    "track_id": track_id,
                    "vehicle_type": vehicle_type,
                    "bbox": (x1, y1, x2, y2),
                    "center": (cx, cy),
                    "frame": frame_index
                })

            return tracked_objects

        except Exception as e:
            print(f"Error in process_frame: {e}")
            return []

    # --------------------------------------------------
    # COUNTING LOGIC
    # --------------------------------------------------
    def update_counts(self, track_id, vehicle_type):
        """
        Counts a vehicle only once based on unique track ID.
        """
        try:
            if track_id not in self.seen_ids:
                self.seen_ids.add(track_id)
                if vehicle_type in self.vehicle_counts:
                    self.vehicle_counts[vehicle_type] += 1
        except Exception as e:
            print(f"Error in update_counts: {e}")

    # --------------------------------------------------
    # TRACK HISTORY
    # --------------------------------------------------
    def update_track_history(self, track_id, center_point):
        """
        Stores center points for each track ID.
        """
        try:
            if track_id not in self.track_history:
                self.track_history[track_id] = []
            self.track_history[track_id].append(center_point)
        except Exception as e:
            print(f"Error in update_track_history: {e}")

    # --------------------------------------------------
    # CLASS MAPPING
    # --------------------------------------------------
    def map_class(self, class_id):
        """
        Maps COCO class IDs to project vehicle categories.
        """
        try:
            coco_mapping = {
                2: "car",    # car
                3: "bike",   # motorcycle
                1: "bike",   # bicycle
                5: "bus",    # bus
                7: "truck"   # truck
            }
            return coco_mapping.get(class_id, None)
        except Exception as e:
            print(f"Error in map_class: {e}")
            return None

    # --------------------------------------------------
    # GETTERS
    # --------------------------------------------------
    def get_counts(self):
        try:
            return self.vehicle_counts
        except Exception as e:
            print(f"Error in get_counts: {e}")
            return {}

    def get_track_history(self):
        try:
            return self.track_history
        except Exception as e:
            print(f"Error in get_track_history: {e}")
            return {}
