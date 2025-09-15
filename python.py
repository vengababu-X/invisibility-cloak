# red_invisibility_no_border.py
import cv2
import numpy as np
import time
import traceback

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: cannot open webcam (close other apps that use camera).")
        return

    # Warmup
    time.sleep(1)
    print("Move out of the frame for ~5 seconds so the script can capture the background...")

    # Capture and average several frames for stable background
    acc = None
    frames_to_capture = 60
    captured = 0
    for i in range(frames_to_capture):
        ret, bg = cap.read()
        if not ret:
            continue
        bg = cv2.flip(bg, 1)
        if acc is None:
            acc = bg.astype(np.float32)
        else:
            acc += bg.astype(np.float32)
        captured += 1
        time.sleep(0.02)
    if captured == 0:
        print("Error: Could not capture background frames.")
        cap.release()
        return
    background = (acc / captured).astype(np.uint8)
    print("Background captured ✅  — now put on your RED T-shirt and step into the frame.")
    print("Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)

            if background.shape != frame.shape:
                background = cv2.resize(background, (frame.shape[1], frame.shape[0]))

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # --- RED ranges (two zones in HSV) ---
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])

            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)

            # --- clean the mask ---
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

            # --- smooth alpha for soft edges ---
            mask_blur = cv2.GaussianBlur(mask, (31, 31), 0)
            alpha = (mask_blur.astype(np.float32) / 255.0)
            alpha_3 = cv2.merge([alpha, alpha, alpha])

            # blend
            fg = frame.astype(np.float32)
            bgf = background.astype(np.float32)
            out = (alpha_3 * bgf + (1.0 - alpha_3) * fg).astype(np.uint8)

            # show
            cv2.imshow("Mask (binary)", mask)
            cv2.imshow("Red Invisibility (no border)", out)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception:
        traceback.print_exc()
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
