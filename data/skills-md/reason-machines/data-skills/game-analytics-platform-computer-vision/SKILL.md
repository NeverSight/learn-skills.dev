---
name: game-analytics-platform-computer-vision
description: Real-time computer vision fitness game platform using YOLO, MediaPipe, Spring Boot orchestration, and React dashboard for webcam-based exercise tracking
triggers:
  - how do I set up the game analytics platform
  - create a new computer vision exercise game
  - integrate YOLO tracking with MediaPipe pose detection
  - build a fitness tracking game with webcam
  - manage Python AI processes from Spring Boot
  - export exercise metrics to CSV from vision data
  - configure real-time pose estimation game
  - add text-to-speech coaching to workout tracker
---

# Game Analytics Platform - Computer Vision Fitness Tracker

> Skill by [ara.so](https://ara.so) — Data Skills collection.

## What This Project Does

Game Analytics Platform is a local-first, real-time computer vision system that tracks user movements across 16 fitness exercises using webcam input. It combines:

- **YOLO v8** for object detection and tracking (balls, cones, people)
- **MediaPipe** for skeletal pose estimation and form validation
- **Spring Boot** (Java 17) backend for process orchestration
- **React + Vite** frontend dashboard for game control
- **Python AI scripts** that export workout metrics to CSV
- **pyttsx3** for real-time audio coaching

The architecture runs entirely locally with a 3-tier design: React UI → Spring Boot API → Python AI processes.

## Installation

### Prerequisites

Install these first:
- **Python 3.10+** (ensure "Add to PATH" is checked)
- **Java 17** (from Adoptium)
- **Node.js LTS**

### Auto-Install

```bash
# Windows
python install.py

# Mac/Linux
python3 install.py
```

This creates a Python virtual environment, installs dependencies, downloads YOLO models, and builds the frontend.

### Manual Setup (if auto-install fails)

```bash
# 1. Create Python virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install ultralytics mediapipe opencv-python pandas pyttsx3

# 4. Build frontend
cd frontend
npm install
npm run build
cd ..

# 5. Build backend
cd backend
mvn clean package
cd ..
```

## Starting the Platform

```bash
# Windows
start.bat

# Mac/Linux
./start.sh
```

Access dashboard at `http://localhost:8080`

## Architecture Components

### 1. Spring Boot Backend (Java)

The backend orchestrates Python AI processes via REST API.

**Key Files:**
- `backend/src/main/java/com/gameanalytics/controller/GameController.java`
- `backend/src/main/java/com/gameanalytics/service/ProcessService.java`

**REST API Endpoints:**

```java
// Start a game
POST /api/games/{id}/start
// Response: 200 OK or 400 if game already running

// Stop a game
POST /api/games/{id}/stop
// Response: 200 OK

// Get available CSV data files
GET /api/games/data
// Response: ["workout_20260601_143022.csv", ...]

// Get list of all games
GET /api/games
// Response: [{"id": 1, "name": "YOLO Ball Counter", ...}, ...]
```

**Process Management Pattern:**

```java
// ProcessService.java
public class ProcessService {
    private Process currentProcess;
    private final Object lock = new Object();

    public boolean startGame(int gameId) {
        synchronized (lock) {
            if (currentProcess != null && currentProcess.isAlive()) {
                return false; // Game already running
            }
            
            String pythonPath = System.getProperty("os.name").toLowerCase().contains("win")
                ? "venv\\Scripts\\python.exe"
                : "venv/bin/python";
            
            String scriptPath = "games/exe_" + gameId + ".py";
            
            ProcessBuilder pb = new ProcessBuilder(pythonPath, scriptPath);
            pb.directory(new File(System.getProperty("user.dir")));
            pb.redirectErrorStream(true);
            
            try {
                currentProcess = pb.start();
                
                // Stream logs asynchronously
                new Thread(() -> {
                    try (BufferedReader reader = new BufferedReader(
                            new InputStreamReader(currentProcess.getInputStream()))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            System.out.println("[Python] " + line);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }).start();
                
                return true;
            } catch (IOException e) {
                e.printStackTrace();
                return false;
            }
        }
    }

    public boolean stopGame() {
        synchronized (lock) {
            if (currentProcess != null && currentProcess.isAlive()) {
                currentProcess.destroy();
                try {
                    currentProcess.waitFor(5, TimeUnit.SECONDS);
                } catch (InterruptedException e) {
                    currentProcess.destroyForcibly();
                }
                currentProcess = null;
                return true;
            }
            return false;
        }
    }
}
```

### 2. Python AI Vision Scripts

Each game is a standalone Python script in `games/exe_*.py`.

**Template for New Game:**

```python
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import mediapipe as mp
import pyttsx3
import signal
import sys
from datetime import datetime
import threading

# Global state
running = True
event_buffer = []
tts_engine = None

def signal_handler(sig, frame):
    """Handle SIGTERM from Java backend"""
    global running
    print("Received stop signal, cleaning up...")
    running = False

def tts_worker(queue):
    """Async text-to-speech thread"""
    global tts_engine
    tts_engine = pyttsx3.init()
    while running:
        if not queue.empty():
            message = queue.get()
            tts_engine.say(message)
            tts_engine.runAndWait()

def main():
    global running, event_buffer
    
    # Register signal handler
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize models
    yolo_model = YOLO('models/yolov8n.pt')  # Nano model for speed
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Start TTS thread
    from queue import Queue
    tts_queue = Queue()
    tts_thread = threading.Thread(target=tts_worker, args=(tts_queue,))
    tts_thread.daemon = True
    tts_thread.start()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam")
        return
    
    # Game state
    rep_count = 0
    last_state = None
    
    print("Starting game loop...")
    
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize for performance
        frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # YOLO object detection
        yolo_results = yolo_model.track(frame, persist=True, verbose=False)
        
        # MediaPipe pose detection
        pose_results = pose.process(rgb_frame)
        
        # Game logic example: squat counter
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            
            # Get hip and knee angles
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            
            # Calculate knee angle (simplified)
            hip_y = left_hip.y
            knee_y = left_knee.y
            angle = abs(hip_y - knee_y) * 100  # Normalize to 0-100
            
            # State machine
            if angle < 30 and last_state != 'down':
                last_state = 'down'
            elif angle > 70 and last_state == 'down':
                rep_count += 1
                last_state = 'up'
                tts_queue.put(f"Rep {rep_count}")
                event_buffer.append({
                    'timestamp': datetime.now().isoformat(),
                    'event': 'rep_completed',
                    'count': rep_count,
                    'angle': angle
                })
            
            # Draw skeleton
            mp.solutions.drawing_utils.draw_landmarks(
                frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )
        
        # Draw UI overlay
        cv2.putText(frame, f"Reps: {rep_count}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        
        cv2.imshow('Game', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Export data
    if event_buffer:
        df = pd.DataFrame(event_buffer)
        output_file = f"data/workout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved workout data to {output_file}")
    
    print("Game stopped cleanly")

if __name__ == "__main__":
    main()
```

### 3. React Frontend

**API Integration Pattern:**

```javascript
// frontend/src/services/gameService.js
const API_BASE = 'http://localhost:8080/api/games';

export const startGame = async (gameId) => {
  const response = await fetch(`${API_BASE}/${gameId}/start`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'Failed to start game');
  }
  
  return response.json();
};

export const stopGame = async (gameId) => {
  const response = await fetch(`${API_BASE}/${gameId}/stop`, {
    method: 'POST',
  });
  
  return response.json();
};

export const getWorkoutData = async () => {
  const response = await fetch(`${API_BASE}/data`);
  return response.json();
};

// Polling pattern for CSV updates
export const pollForNewData = (callback, interval = 2000) => {
  const poller = setInterval(async () => {
    const files = await getWorkoutData();
    callback(files);
  }, interval);
  
  return () => clearInterval(poller);
};
```

## Configuration

Each game has a JSON config in `configs/game_{id}.json`:

```json
{
  "game_id": 1,
  "name": "YOLO Ball Counter",
  "yolo_model": "models/yolov8n.pt",
  "confidence_threshold": 0.5,
  "tracking_persistence": true,
  "audio_coaching": true,
  "target_fps": 30,
  "resolution": [640, 480],
  "coaching_triggers": {
    "milestone_reps": [5, 10, 20],
    "form_warning_angle": 45
  }
}
```

**Loading config in Python:**

```python
import json

def load_game_config(game_id):
    with open(f'configs/game_{game_id}.json', 'r') as f:
        return json.load(f)

config = load_game_config(1)
yolo_model = YOLO(config['yolo_model'])
confidence = config['confidence_threshold']
```

## Common Patterns

### 1. Adding a New Exercise Game

```bash
# 1. Create Python script
touch games/exe_17.py

# 2. Create config
cat > configs/game_17.json << EOF
{
  "game_id": 17,
  "name": "Jumping Jacks Counter",
  "yolo_model": "models/yolov8n-pose.pt",
  "confidence_threshold": 0.6
}
EOF

# 3. Update backend game list
# Edit: backend/src/main/resources/games.json
# Add: {"id": 17, "name": "Jumping Jacks Counter", "description": "..."}
```

### 2. Combining YOLO + MediaPipe

```python
# Detect objects with YOLO, track pose with MediaPipe
yolo_results = yolo_model(frame)
pose_results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# Example: Check if person's hand crosses detected ball
if pose_results.pose_landmarks and len(yolo_results) > 0:
    hand = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value]
    
    for detection in yolo_results[0].boxes:
        if detection.cls == 32:  # Sports ball class
            ball_x, ball_y = detection.xywh[0][:2]
            hand_x = hand.x * frame.shape[1]
            hand_y = hand.y * frame.shape[0]
            
            distance = np.sqrt((hand_x - ball_x)**2 + (hand_y - ball_y)**2)
            if distance < 50:  # Pixels
                print("Hand touched ball!")
```

### 3. CSV Data Export Pattern

```python
# Track events during game
event_buffer = []

# During game loop
event_buffer.append({
    'timestamp': datetime.now().isoformat(),
    'event_type': 'crossing',
    'player_position_x': x,
    'player_position_y': y,
    'speed_estimate': speed,
    'rep_count': reps
})

# On game stop
df = pd.DataFrame(event_buffer)
df['session_id'] = datetime.now().strftime('%Y%m%d_%H%M%S')
df.to_csv(f"data/workout_{df['session_id'].iloc[0]}.csv", index=False)
```

### 4. Thread-Safe Audio Coaching

```python
from queue import Queue
import threading
import pyttsx3

def tts_worker(queue):
    engine = pyttsx3.init()
    while True:
        message = queue.get()
        if message is None:
            break
        engine.say(message)
        engine.runAndWait()
        queue.task_done()

tts_queue = Queue()
tts_thread = threading.Thread(target=tts_worker, args=(tts_queue,))
tts_thread.daemon = True
tts_thread.start()

# In game loop
if rep_count % 5 == 0:
    tts_queue.put(f"Great job! {rep_count} reps completed")
```

## Troubleshooting

### Python Process Won't Stop

```java
// In ProcessService.java, add forceful termination
public boolean stopGame() {
    synchronized (lock) {
        if (currentProcess != null && currentProcess.isAlive()) {
            currentProcess.destroy();
            try {
                if (!currentProcess.waitFor(3, TimeUnit.SECONDS)) {
                    currentProcess.destroyForcibly();
                    currentProcess.waitFor(2, TimeUnit.SECONDS);
                }
            } catch (InterruptedException e) {
                currentProcess.destroyForcibly();
            }
            currentProcess = null;
            return true;
        }
        return false;
    }
}
```

### Webcam Not Found

```python
# Test all camera indices
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        cap.release()
        break
```

### YOLO Model Loading Fails

```python
import os
from ultralytics import YOLO

model_path = 'models/yolov8n.pt'

if not os.path.exists(model_path):
    print("Downloading YOLO model...")
    model = YOLO('yolov8n.pt')  # Auto-downloads
    os.makedirs('models', exist_ok=True)
    # Model cached in ultralytics directory
else:
    model = YOLO(model_path)
```

### CORS Issues (if running frontend separately)

```java
// backend/src/main/java/com/gameanalytics/config/WebConfig.java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:5173")  // Vite dev server
                .allowedMethods("GET", "POST", "PUT", "DELETE");
    }
}
```

### CSV Not Appearing in Frontend

```javascript
// Ensure polling starts after game stops
const handleStopGame = async (gameId) => {
  await stopGame(gameId);
  
  // Wait for Python to write CSV
  setTimeout(async () => {
    const files = await getWorkoutData();
    setWorkoutFiles(files);
  }, 2000);
};
```

## Performance Optimization

```python
# Use YOLO tracking instead of detection for speed
results = model.track(frame, persist=True, tracker="bytetrack.yaml")

# Reduce frame processing
frame_skip = 2
frame_count = 0

while running:
    ret, frame = cap.read()
    frame_count += 1
    
    if frame_count % frame_skip != 0:
        continue  # Process every 2nd frame
    
    # Your inference code...
```

## Environment Variables

```bash
# .env (create in project root)
YOLO_MODEL_PATH=models/yolov8n.pt
MEDIAPIPE_MODEL_COMPLEXITY=1
TTS_RATE=150
WEBCAM_INDEX=0
OUTPUT_DIR=data
```

```python
# Load in Python
import os
from dotenv import load_dotenv

load_dotenv()

model_path = os.getenv('YOLO_MODEL_PATH', 'models/yolov8n.pt')
webcam_index = int(os.getenv('WEBCAM_INDEX', '0'))
```
