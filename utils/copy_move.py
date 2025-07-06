import os
import cv2
import numpy as np

def detect_copy_move(image_path, output_folder):
    output_path = os.path.join(output_folder, 'copy_move.jpg')
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        return "Invalid", None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)

    if descriptors is None or len(keypoints) < 10:
        return "Authentic", output_path.replace('static/', '')

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors, descriptors, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance and m.queryIdx != m.trainIdx]

    result = image.copy()
    for match in good_matches:
        pt1 = tuple(np.round(keypoints[match.queryIdx].pt).astype(int))
        pt2 = tuple(np.round(keypoints[match.trainIdx].pt).astype(int))
        cv2.line(result, pt1, pt2, (0, 255, 0), 1)

    cv2.imwrite(output_path, result)

    # Verdict logic
    if len(good_matches) > 30:
        return "Forged", output_path.replace('static/', '')
    elif len(good_matches) > 15:
        return "Suspicious", output_path.replace('static/', '')
    else:
        return "Authentic", output_path.replace('static/', '')
