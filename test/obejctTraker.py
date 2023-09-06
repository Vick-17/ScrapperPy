import cv2
import numpy as np

# Initialiser le tracker
tracker = cv2.TrackerKCF_create()

# Capturer le flux en direct à partir de l'URL
video = cv2.VideoCapture("https://www.youtube.com/watch?v=z545k7Tcb5o&ab_channel=PeripheriqueNord")

ret, frame = video.read()
bbox = cv2.selectROI("Tracking", frame, False)

tracker.init(frame, bbox)

while True:
    ret, frame = video.read()
    if not ret:
        break
    success, bbox = tracker.update(frame)
    
    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
       cv2.putText(frame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.imshow("Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()
