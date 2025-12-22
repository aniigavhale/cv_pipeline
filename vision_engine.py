import cv2

class VisionEngine:
    def __init__(self):
        # Initialize the background frame for motion detection
        self.avg = None

    def detect_motion(self, frame):
        # Part 1: Image Processing (Grayscale & Blur)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.avg is None:
            self.avg = gray.copy().astype("float")
            return False, 0

        # Part 2: Event Detection Logic
        # Accumulate the weighted average to handle light changes
        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        
        # Threshold the delta image to find regions with motion
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        motion_area = 0
        for c in contours:
            if cv2.contourArea(c) < 5000: # Sensitivity threshold
                continue
            motion_detected = True
            motion_area = cv2.contourArea(c)
            
        return motion_detected, motion_area