# Traffic Analytics System

This project implements an end-to-end traffic analytics pipeline using a fixed-camera road/gate video.
The system performs vehicle detection, tracking, direction analysis, speed estimation, and result logging in a modular and extensible manner.

---

## 🚀 Features

- Vehicle detection using YOLOv8
- Multi-object tracking using BoT-SORT
- Vehicle classification (car, bike/two-wheeler, bus, truck)
- Direction of travel detection (IN / OUT) for top-down camera views
- Speed estimation using pixel-to-meter approximation with perspective handling
- Annotated output video with:
  - Thin bounding boxes
  - Vehicle ID, class, direction, and speed
  - Per-class vehicle counts and total count
- Structured CSV outputs:
  - Per-vehicle results
  - Speed summary and vehicle count statistics
- Clean OOP-based architecture with no global variables
- Robust error handling using `try-except` blocks
- Optional web-based demo using Streamlit for interactive execution

---

## 🔄 Pipeline Overview

1. Input video is read frame-by-frame from a fixed camera source.
2. Vehicles are detected using a YOLOv8 object detection model.
3. Detected vehicles are tracked across frames using the BoT-SORT tracker.
4. Each vehicle is assigned a unique track ID and classified by type.
5. Direction of movement (IN / OUT) is determined using net vertical displacement.
6. Speed is estimated using pixel-to-meter approximation with perspective handling.
7. Results are logged into structured CSV files.
8. An annotated output video is generated with visual overlays.

---

## 📁 Project Structure
```
traffic-analytics-system/
│
├── src/
│   ├── detector_tracker.py
│   ├── direction_analyzer.py
│   ├── speed_estimator.py
│   ├── result_logger.py
│   └── pipeline.py
│
├── tests/
│   ├── test_direction_analyzer.py
│   └── test_speed_estimator.py
│
├── data/
│   └── input/
│       └── video.mp4
│
├── output/
│   ├── annotated_video.mp4
│   ├── results.csv
│   └── speed_summary.csv
│
├──report/
│   └── Traffic_Analytics_System_Report.pdf
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
---

## 🧰 Technologies Used

- Python – Core programming language
- YOLOv8 (Ultralytics) – Vehicle detection
- BoT-SORT – Multi-object tracking
- OpenCV – Video processing and visualization
- NumPy – Numerical computations
- Pandas – CSV generation and data handling
- PyTest – Unit testing framework
- Streamlit – Lightweight web-based demo interface

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/arshita15/traffic-analytics-system.git
cd traffic-analytics-system
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
---

## 🧪 Running Unit Tests

Basic unit tests are provided to validate core analytical components:
 - Direction analysis logic
 - Speed estimation logic

### Test requirements
The tests use pytest.

### Run all tests
From the project root, run:

```bash
pytest
```

### Run a specific test file

```bash
pytest tests/test_direction_analyzer.py
pytest tests/test_speed_estimator.py

```
---

## ▶️ Running the Pipeline

### Place your input video at:

```
data/input/video.mp4
```

### Run the pipeline from the project root:

```bash
python -m src.pipeline
```

---

## 🌐 Web Demo Deployment (Streamlit)

In addition to the command-line pipeline, a lightweight web-based demo is provided using Streamlit.

### How to run the web app
```bash
streamlit run app.py
```

### Usage:
- Upload any traffic video (.mp4)
- Click Run Traffic Analysis
- The pipeline executes locally
- Outputs are generated in the output/ directory

Note: Uploaded videos are internally saved as data/input/video.mp4 for pipeline compatibility.

---

## 📤 Outputs

After execution, the following outputs are generated:

### Annotated Video

```
output/annotated_video.mp4

```
The video contains bounding boxes, vehicle metadata, and live vehicle counts.

### Per-Vehicle Results

```
output/results.csv

```
Columns include:
- Serial number
- Track ID
- Vehicle type
- Direction (IN / OUT)
- Average moving speed (km/h)
- Start frame
- End frame

### Speed Summary

```
output/speed_summary.csv

```
Includes:
- Average speed per vehicle category
- Speed distribution
- Vehicle counts per category
- Total vehicle count

---

## 📝 Notes

This README provides an overview of the project structure and usage.  
The current implementation performs inference on CPU, which can result in longer processing times for high-resolution videos.
The detailed project report is available in the `report/` directory..







