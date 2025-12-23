# -------- Motion-aware background update params --------
bg_alpha = 0.02          # slow update rate
motion_thresh = 25

prev_gray = None

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)

    if prev_gray is None:
        prev_gray = gray.copy()

    diff = cv2.absdiff(prev_gray, gray)
    _, motion_mask = cv2.threshold(diff, motion_thresh, 255, cv2.THRESH_BINARY)
    motion_mask = cv2.dilate(motion_mask, None, iterations=2)
    prev_gray = gray.copy()

    # -------- Mask selection (same modes as before) --------
    if mode == 1:
        lower = np.clip(target_hsv - tolerance, [0,0,0], [180,255,255])
        upper = np.clip(target_hsv + tolerance, [180,255,255], [180,255,255])
        cloak_mask = cv2.inRange(hsv, lower, upper)

    elif mode == 2:
        roi = hsv[h//2-40:h//2+40, w//2-40:w//2+40]
        Z = roi.reshape((-1,3)).astype(np.float32)
        _, labels, centers = cv2.kmeans(
            Z, 2, None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
            10, cv2.KMEANS_RANDOM_CENTERS
        )
        dominant = centers[np.bincount(labels.flatten()).argmax()]
        lower = np.clip(dominant - tolerance, [0,0,0], [180,255,255])
        upper = np.clip(dominant + tolerance, [180,255,255], [180,255,255])
        cloak_mask = cv2.inRange(hsv, lower, upper)

    else:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = segmentor.process(rgb)
        cloak_mask = (result.segmentation_mask < 0.5).astype(np.uint8) * 255

    # -------- Mask cleanup --------
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    cloak_mask = cv2.morphologyEx(cloak_mask, cv2.MORPH_OPEN, kernel)
    cloak_mask = cv2.morphologyEx(cloak_mask, cv2.MORPH_DILATE, kernel)

    # -------- Adaptive background update (key part) --------
    static_area = cv2.bitwise_not(motion_mask)
    bg_update_mask = cv2.bitwise_and(static_area, cv2.bitwise_not(cloak_mask))

    bg_float = background.astype(np.float32)
    frame_float = frame.astype(np.float32)

    update = bg_update_mask.astype(np.float32) / 255.0
    update = cv2.merge([update, update, update])

    background = (
        bg_float * (1 - bg_alpha * update) +
        frame_float * (bg_alpha * update)
    ).astype(np.uint8)

    # -------- Soft blending --------
    mask_blur = cv2.GaussianBlur(cloak_mask, (21,21), 0)
    alpha = cv2.merge([mask_blur/255]*3)

    output = (alpha * background + (1 - alpha) * frame).astype(np.uint8)

    cv2.putText(
        output,
        f"Mode: {['HSV','KMeans','ML'][mode-1]} | B: Reset BG",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.imshow("Universal Invisibility Cloak++", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'): mode = 1
    if key == ord('2'): mode = 2
    if key == ord('3'): mode = 3
    if key == ord('b'): background = frame.copy()
    if key == ord('q'): break
