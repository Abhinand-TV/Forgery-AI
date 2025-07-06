from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt

def perform_ela(image_path, output_path="static/result.jpg"):
    original = Image.open(image_path).convert("RGB")
    compressed_path = "static/compressed.jpg"
    original.save(compressed_path, "JPEG", quality=90)
    compressed = Image.open(compressed_path)

    diff = ImageChops.difference(original, compressed)
    diff = np.array(diff) * 10  # amplify difference
    ela_img = Image.fromarray(np.uint8(np.clip(diff, 0, 255)))
    ela_img.save(output_path)

    # Use standard deviation instead of mean for robustness
    std_dev = np.std(diff)
    threshold = 22  # you can experiment with 18–25 for best results

    return "Forged" if std_dev > threshold else "Genuine"
