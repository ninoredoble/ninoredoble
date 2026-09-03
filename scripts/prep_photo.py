import sys
import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

INP = sys.argv[1] if len(sys.argv) > 1 else img/GNEGR.png
OUT = sys.argv[2] if len(sys.argv) > 2 else source-prepped.png

# 1. Background removal
img = Image.open(INP)
cut = remove(img)

# 2. Separate RGB and Alpha
cut_np = np.array(cut)
rgb = cut_np[:, :, :3]
alpha = cut_np[:, :, 3]

# 3. Apply CLAHE on L-channel in LAB space for local contrast
lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
l, a, b = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
l_clahe = clahe.apply(l)
lab_enhanced = cv2.merge((l_clahe, a, b))
rgb_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)

# 4. Composite onto pure white background
white_bg = np.full_like(rgb_enhanced, 255)
alpha_factor = (alpha / 255.0)[:, :, np.newaxis]
final = (rgb_enhanced * alpha_factor + white_bg * (1 - alpha_factor)).astype(np.uint8)

Image.fromarray(final).save(OUT)
print(fPrepped photo written to {OUT})
