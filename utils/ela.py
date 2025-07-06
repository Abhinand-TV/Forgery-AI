import os
from PIL import Image, ImageChops, ImageEnhance

def perform_ela(image_path, output_folder):
    ela_path = os.path.join(output_folder, 'ela_result.jpg')

    temp_path = os.path.join(output_folder, 'temp_compressed.jpg')
    image = Image.open(image_path).convert('RGB')
    image.save(temp_path, 'JPEG', quality=90)

    compressed = Image.open(temp_path)
    ela_image = ImageChops.difference(image, compressed)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])

    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    ela_image.save(ela_path)

    # Verdict logic
    ela_verdict = "Authentic"
    if max_diff > 50:
        ela_verdict = "Forged"
    elif max_diff > 30:
        ela_verdict = "Suspicious"

    return ela_verdict, ela_path.replace('static/', '')