import csv
import os


class ResultLogger:
    def __init__(self, output_dir="output"):
        try:
            self.output_dir = output_dir
            os.makedirs(self.output_dir, exist_ok=True)

            self.results_path = os.path.join(self.output_dir, "results.csv")
            self.speed_summary_path = os.path.join(self.output_dir, "speed_summary.csv")

        except Exception as e:
            print(f"Error in ResultLogger.__init__: {e}")

    # ---------------- RESULTS ----------------
    def write_results(self, results):
        try:
            if not results:
                print("DEBUG: No results to write")
                return

            with open(self.results_path, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "s_no",
                        "track_id",
                        "vehicle_type",
                        "direction",
                        "speed_kmph",
                        "start_frame",
                        "end_frame"
                    ]
                )
                writer.writeheader()

                for r in results:
                    writer.writerow({
                        "s_no": r["s_no"],
                        "track_id": r["track_id"],
                        "vehicle_type": r["vehicle_type"],
                        "direction": r["direction"],
                        "speed_kmph": r["speed"],
                        "start_frame": r["start_frame"],
                        "end_frame": r["end_frame"]
                    })

            print("DEBUG: results.csv written")

        except Exception as e:
            print(f"Error in write_results: {e}")

    # ---------------- SUMMARY ----------------
    def write_speed_summary(self, speed_summary, vehicle_counts):
        try:
            with open(self.speed_summary_path, "w", newline="") as f:
                writer = csv.writer(f)

                writer.writerow(["SPEED SUMMARY"])
                writer.writerow([
                    "vehicle_type",
                    "average_speed",
                    "0-20",
                    "20-40",
                    "40-60",
                    "60+"
                ])

                for vt, data in speed_summary.items():
                    d = data["distribution"]
                    writer.writerow([
                        vt,
                        data["average_speed"],
                        d["0-20"],
                        d["20-40"],
                        d["40-60"],
                        d["60+"]
                    ])

                writer.writerow([])
                writer.writerow(["VEHICLE COUNTS"])
                writer.writerow(["vehicle_type", "count"])

                total = 0
                for vt, c in vehicle_counts.items():
                    writer.writerow([vt, c])
                    total += c

                writer.writerow(["TOTAL", total])

            print("DEBUG: speed_summary.csv written")

        except Exception as e:
            print(f"Error in write_speed_summary: {e}")
