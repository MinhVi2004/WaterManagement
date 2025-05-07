import os
# Buộc segmentation_models dùng tf.keras
os.environ["SM_FRAMEWORK"] = "tf.keras"

import segmentation_models as sm
import tensorflow as tf
# Xác nhận framework
sm.set_framework("tf.keras")

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes
from skimage.measure import label, regionprops

# Đơn giản hóa: chỉ phần segmentation

# Các đường dẫn
CSV_PATH = 'H:/My Drive/WaterMeters/data.csv'
IMAGES_FOLDER = 'H:/My Drive/WaterMeters/images'
MASKS_FOLDER = 'H:/My Drive/WaterMeters/masks'

IMAGE_PATH = 'H:/My Drive/WaterMeters/images/id_1_value_13_116.jpg'
MODEL_PATH = 'H:/My Drive/WaterMeters/final_segmentation_model.h5'
# Load DataFrame và in thông tin
data = pd.read_csv(CSV_PATH)
print(f'Total images: {len(os.listdir(IMAGES_FOLDER))}')
print(f'Total masks: {len(os.listdir(MASKS_FOLDER))}')
print(f'Dataset length: {len(data)}')

# Load segmentation model (không compile tự động)
model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={
        'binary_crossentropy_plus_jaccard_loss': sm.losses.bce_jaccard_loss,
        'iou_score': sm.metrics.iou_score
    },
    compile=False
)
# Compile thủ công
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss=sm.losses.bce_jaccard_loss,
    metrics=[sm.metrics.iou_score]
)

# Hàm dự đoán mask
def predict_mask(model, image, target_size=(224, 224)):
    img = cv2.resize(image, target_size) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)[0]
    mask = (pred > 0.5).astype(np.uint8)
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    return mask

# Hàm xử lý mask
def process_mask(mask):
    filled = binary_fill_holes(mask).astype(np.uint8)
    kernel = np.ones((3,3), np.uint8)
    cleaned = cv2.morphologyEx(filled, cv2.MORPH_OPEN, kernel, iterations=2)
    return cleaned

# Hàm crop region chứa số
def extract_digits_region(image, mask):
    labeled = label(mask)
    regions = regionprops(labeled)
    largest = max(regions, key=lambda r: r.area, default=None)
    if largest:
        minr, minc, maxr, maxc = largest.bbox
        return image[minr:maxr, minc:maxc]
    print("No valid region found.")
    return None

# Thực thi pipeline
# image = cv2.imread(IMAGE_PATH)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# mask = predict_mask(model, image)
# mask_cleaned = process_mask(mask)
# cropped = extract_digits_region(image, mask_cleaned)

# Hiển thị kết quả
def show_results(image_path):
      image = cv2.imread(image_path)
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      mask = predict_mask(model, image)
      mask_cleaned = process_mask(mask)
      cropped = extract_digits_region(image, mask_cleaned)
      
      
      plt.figure(figsize=(12, 4))
      plt.subplot(1, 3, 1)
      plt.imshow(image)
      plt.title('Original')
      plt.axis('off')

      plt.subplot(1, 3, 2)
      plt.imshow(mask, cmap='gray')
      plt.title('Processed Mask')
      plt.axis('off')

      plt.subplot(1, 3, 3)
      if cropped is not None:
            plt.imshow(cropped)
            plt.title('Cropped Digits')
      else:
            plt.text(0.5, 0.5, 'No region to crop', ha='center')
            plt.title('Cropped Digits')
      plt.axis('off')

      plt.tight_layout()
      plt.show()

show_results(IMAGE_PATH)
