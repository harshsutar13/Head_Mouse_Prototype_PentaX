🖱️ Head Mouse – A Vision-Based Hands-Free Interaction System
📌 Overview

Head Mouse is a vision-based hands-free computer interaction system that allows users to control a computer without using traditional input devices such as a mouse or keyboard. The system uses eye movements for cursor control, eye blinks for mouse click operations, and voice commands for typing and basic system actions. The project is developed as a working desktop prototype using a webcam and microphone.

====================================================================================================================

❓ Problem Statement

Traditional computer interaction techniques mainly depend on mouse and keyboard, which require physical movement and fine motor control. These methods are not suitable for people with physical disabilities or motor impairments and are also inconvenient in hands-free environments. Existing assistive solutions often rely on expensive hardware, wearable sensors, or electrical signal sensing chips, making them less accessible and costly.

====================================================================================================================

💡 Proposed Solution

This project provides a reliable, effortless, and user-friendly hands-free interaction system. Eye movements are used to control the cursor, eye blinks are used for mouse clicks, and voice commands are used for typing and system-level operations. The solution works using only a standard webcam and microphone, eliminating the need for special hardware. The system is modular and designed to be extended to smart wearable devices and AR/VR platforms in the future.

====================================================================================================================

✨ Key Features (Prototype)

Hands-free cursor control using real-time eye tracking

Mouse click using eye blink detection

Smooth cursor movement with motion smoothing

Automatic blink threshold calibration

Voice commands for typing text

Voice-based opening of applications and websites

Voice commands for scrolling and navigation

Real-time response with minimal latency

Software-based solution using webcam and microphone

No wearable devices or external hardware required

Modular architecture with eye and voice control running in parallel

User-friendly interaction system

Supports English and Marathi voice input

AI-powered question answering using Groq API

Helpful for people with physical disabilities and motor impairments

====================================================================================================================

🧠 Technologies Used

Python – Core programming language

OpenCV – Video capture and image processing

Google MediaPipe – Face and eye landmark detection

NumPy – Mathematical computations and smoothing

PyAutoGUI – Cursor movement and mouse/keyboard actions

SpeechRecognition (Google Speech-to-Text) – Voice command processing

CustomTkinter – System controller GUI

Groq API – AI-based text generation (optional feature)

====================================================================================================================

🏗️ System Architecture

The system consists of two parallel modules:

Eye Control Module – Handles eye tracking and blink detection for cursor movement and mouse clicks.

Voice Control Module – Handles speech recognition, command processing, and typing actions.

Both modules are managed by a System Controller, which runs them simultaneously using multithreading and executes actions on the operating system.

====================================================================================================================

🔄 Process Flow

User provides eye movement, blink, and voice input

Webcam captures facial video and microphone captures voice

Eye data is processed using MediaPipe for tracking and blink detection

Voice input is converted to text using speech recognition

Commands are interpreted and passed to the system controller

Cursor movement, clicks, typing, and system actions are executed in real time

====================================================================================================================

🚀 Future Scope

Improved accuracy using learning-based gaze estimation

Personalized user calibration

Multi-language voice support

Noise-robust voice recognition

Integration with smart glasses and wearable devices

AR/VR headset integration for immersive interaction

Optimization for low-power and edge devices

Cross-platform and mobile support

Advanced accessibility customization

Cloud-based processing and updates

====================================================================================================================

▶️ How to Run the Project
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Set Environment Variables

Create a .env file:

groq_api=YOUR_API_KEY

3️⃣ Run the System
python run.py

📂 Project Structure
Head-Mouse/
├── eye_mouse_control.py
├── speech_typing.py
├── run.py
├── requirements.txt
├── README.md
├── .env.example
├── assets/
│   ├── screenshots/
│   └── diagrams/

====================================================================================================================

🧪 Current Stage

This project is developed as a functional prototype and demonstrates real-time hands-free computer interaction using eye tracking and voice commands.

====================================================================================================================

🏁 Conclusion

Head Mouse demonstrates how vision-based and voice-based interaction can replace traditional input devices and make computer usage more accessible, inclusive, and user-friendly. The project showcases a practical and scalable assistive technology solution with strong potential for future expansion.