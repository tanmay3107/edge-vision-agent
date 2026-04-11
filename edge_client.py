# edge_client.py
import cv2
import base64
import requests
import time

# The URL of your new FastAPI server
API_URL = "http://127.0.0.1:8000/api/v1/analyze"

cap = cv2.VideoCapture(0)
time.sleep(2)  # Let the camera warm up

# Read the first frame to use as a baseline for motion detection
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Cooldown timer to prevent spamming the API
last_api_call = 0
COOLDOWN_SECONDS = 5

print("🎥 Edge Client Active! Watching for motion...")

while cap.isOpened():
    # 1. Motion Detection Math (Absolute difference between frames)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        # Ignore tiny movements (like shadows or a fan)
        if cv2.contourArea(contour) < 5000:
            continue
        
        motion_detected = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 2. If motion is detected and cooldown is over, send to API
    current_time = time.time()
    if motion_detected and (current_time - last_api_call > COOLDOWN_SECONDS):
        print("\n🏃 Motion detected! Sending frame to AI Server...")
        
        # Convert frame to base64 string
        _, buffer = cv2.imencode('.jpg', frame1)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        
        # Shoot it to the server
        try:
            response = requests.post(API_URL, json={"image_base64": jpg_as_text})
            result = response.json()
            
            if result.get("is_threat"):
                print(f"🚨 ALERT FROM SERVER: {result.get('context')}")
            else:
                print("✅ Server says area is clear.")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot reach server. Is server.py running?")
            
        last_api_call = current_time

    # Display the feed
    cv2.imshow("Edge Client (Motion Scanner)", frame1)
    
    # Advance frames
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()