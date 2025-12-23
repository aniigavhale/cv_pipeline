# Real-Time Computer Vision Pipeline

A modular Python application designed to capture live video, process frames for motion detection, and broadcast structured event data to a real-time web interface. 

## 🚀 Technical Approach
[cite_start]This project implements a complete CV pipeline from frame acquisition to data persistence[cite: 5, 6]:

1.  [cite_start]**Image Processing:** Each frame is converted to **Grayscale** and processed with a **Gaussian Blur** (21x21 kernel) to eliminate high-frequency noise that could cause false motion triggers[cite: 4, 5].
2.  **Event Detection:** Instead of simple frame differencing, the system uses a **Weighted Running Average** algorithm. [cite_start]This allows the background model to adapt dynamically to lighting changes, making the system significantly more robust[cite: 5].
3.  **Real-time Communication:** The backend uses **Flask-SocketIO** to broadcast events as structured **JSON** objects. [cite_start]This ensures "push" updates to the frontend without requiring page refreshes[cite: 4, 6].
4.  [cite_start]**Data Storage:** Every detected event is persisted in a local **SQLite** database, recording the precise timestamp, the event type, and the numeric metric (motion area)[cite: 4, 6].

## 🛠️ Setup Instructions
Follow these steps to run the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd cv_project
    ```
2.  **Set up Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install opencv-python flask flask-socketio eventlet
    ```
4.  **Run the Application:**
    ```bash
    python3 app.py
    ```
5.  **Access the Interface:** Navigate to `http://127.0.0.1:5000` in your web browser.

## 📝 Assumptions
- **Static Camera:** The motion detection logic assumes the camera is in a fixed position. [cite_start]Significant camera movement will trigger false positive events[cite: 24].
- [cite_start]**Lighting:** The environment has consistent enough lighting for the Gaussian blur and thresholding logic to distinguish foreground movement from background noise[cite: 5].

## 📈 Potential Improvements
- **Object Classification:** Integrating a lightweight model like YOLOv8-tiny to classify *what* is moving (e.g., distinguishing a person from a pet).
- **Cloud Logging:** Transitioning the SQLite local storage to a cloud-based PostgreSQL instance for centralized data management across multiple nodes.
- [cite_start]**Advanced FPS Optimization:** Implementing a dedicated "Buffer" class to handle frame reading in a separate thread to further increase processing speed[cite: 6].

## 📂 Project Structure
- [cite_start]`app.py`: Main entry point, Flask server, and integration logic[cite: 2, 4].
- [cite_start]`vision_engine.py`: Contains the `VisionEngine` class for CV processing[cite: 4, 5].
- [cite_start]`database.py`: Handles SQLite connection and structured data logging[cite: 4].
- `templates/`: Contains the HTML frontend for the real-time interface.
