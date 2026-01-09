import cv2

from src.detector_tracker import DetectorTracker
from src.direction_analyzer import DirectionAnalyzer
from src.speed_estimator import SpeedEstimator
from src.result_logger import ResultLogger


class TrafficAnalyticsPipeline:
    def __init__(self, video_path, output_video_path, pixels_per_meter, confidence_threshold=0.4):
        self.video_path = video_path
        self.output_video_path = output_video_path
        self.pixels_per_meter = pixels_per_meter

        self.detector = DetectorTracker(confidence_threshold=confidence_threshold)
        self.direction_analyzer = DirectionAnalyzer()
        self.logger = ResultLogger()

        self.speed_estimator = None
        self.start_frames = {}
        self.final_directions = {}

        # ---------------- COUNTING ----------------
        self.counted_ids = set()
        self.class_counts = {
            "car": 0,
            "bike": 0,
            "bus": 0,
            "truck": 0
        }

    def draw_label(self, frame, text, x, y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        t = 1
        (w, h), _ = cv2.getTextSize(text, font, scale, t)
        cv2.rectangle(frame, (x, y - h - 6), (x + w + 4, y), (0, 0, 0), -1)
        cv2.putText(frame, text, (x + 2, y - 2), font, scale, (255, 255, 255), t)

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print("ERROR: Video not opened")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.speed_estimator = SpeedEstimator(
            pixels_per_meter=self.pixels_per_meter,
            fps=fps,
            frame_height=h
        )

        writer = cv2.VideoWriter(
            self.output_video_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (w, h)
        )

        frame_idx = 0
        vehicle_type_map = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            objs = self.detector.process_frame(frame, frame_idx)

            for o in objs:
                tid = o["track_id"]
                vt = o["vehicle_type"]
                x1, y1, x2, y2 = o["bbox"]

                vehicle_type_map[tid] = vt

                # ---------------- COUNT ONCE ----------------
                if tid not in self.counted_ids:
                    self.counted_ids.add(tid)
                    if vt in self.class_counts:
                        self.class_counts[vt] += 1

                if tid not in self.start_frames:
                    self.start_frames[tid] = frame_idx

                pts = self.detector.track_history.get(tid, [])

                if tid not in self.final_directions:
                    d = self.direction_analyzer.analyze_direction(pts)
                    if d != "UNKNOWN":
                        self.final_directions[tid] = d

                speed = self.speed_estimator.estimate_speed(pts)
                self.speed_estimator.add_vehicle_speed(tid, speed)

                label = f"ID:{tid} {vt} {self.final_directions.get(tid,'UNKNOWN')} {speed:.1f}km/h"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                self.draw_label(frame, label, x1, y1)

            # ---------------- DRAW COUNTS ----------------
            y_offset = 30
            for v_type, count in self.class_counts.items():
                self.draw_label(frame, f"{v_type.upper()}: {count}", 10, y_offset)
                y_offset += 22

            total = sum(self.class_counts.values())
            self.draw_label(frame, f"TOTAL: {total}", 10, y_offset)

            writer.write(frame)
            frame_idx += 1

        print("DEBUG: Writing CSV files now...")

        results = []
        s = 1
        for tid, pts in self.detector.get_track_history().items():
            start = self.start_frames.get(tid)
            end = start + len(pts) if start is not None else None

            results.append({
                "s_no": s,
                "track_id": tid,
                "vehicle_type": vehicle_type_map.get(tid),
                "direction": self.final_directions.get(tid, "UNKNOWN"),
                "speed": self.speed_estimator.get_average_speed(tid),
                "start_frame": start,
                "end_frame": end
            })
            s += 1

        self.logger.write_results(results)

        summary = self.speed_estimator.compute_speed_summary(vehicle_type_map)
        self.logger.write_speed_summary(summary, self.detector.get_counts())

        cap.release()
        writer.release()

        print("PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    TrafficAnalyticsPipeline(
        video_path="data/input/video.mp4",
        output_video_path="output/annotated_video.mp4",
        pixels_per_meter=10
    ).run()
