# invisibility-cloak
Red Invisibility Cloak

A Python project that uses OpenCV to create a Harry Potter-style invisibility cloak effect. This version specifically hides red-colored objects, making them appear invisible in front of a webcam.

Features

Detects and hides red objects in real-time.

Uses OpenCV and NumPy for image processing.

Works with a standard webcam.

Adjustable background capture duration for better effect.

Requirements

Python 3.x

OpenCV

NumPy

Install dependencies using:

pip install opencv-python numpy

How to Run

Clone the repository:

git clone  https://vengababu-x.github.io/invisibility-cloak/
cd red-invisibility-cloak


Run the Python script:

python red_invisibility_cloak.py


Follow the on-screen instructions:

Move out of the camera frame for a few seconds to capture the background.

Then, use a red cloth to see the invisibility effect in action.

How It Works

Captures the background.

Detects red color in the video frame.

Replaces red pixels with the background, creating an invisibility effect.

Screenshots / Demo

(Optional: Add images or GIFs showing the effect here.)

License

MIT License – feel free to use and modify the code.
