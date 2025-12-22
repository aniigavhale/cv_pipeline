from flask import Flask, render_template
from flask_socketio import SocketIO
from vision_engine import VisionEngine
from database import EventDB
import cv2
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
db = EventDB()
engine = VisionEngine()

@app.route('/')
def index():
    return "Server is running. Open this page to see events."

def run_flask():
    # Run the web server in the background
    socketio.run(app, port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start Flask/WebSockets in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Main thread: Camera and OpenCV logic
    cap = cv2.VideoCapture(0)
    print("Camera opening... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect motion using the engine
        is_motion, value = engine.detect_motion(frame)
        
        if is_motion:
            # Part 3 & 4: Save to DB and broadcast via Socket
            event_data = db.log_event("Motion Detected", value)
            socketio.emit('new_event', event_data)
            print(f"Motion Event: {event_data}")

        # Show the video stream
        cv2.imshow("Assignment - Press Q to Exit", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()