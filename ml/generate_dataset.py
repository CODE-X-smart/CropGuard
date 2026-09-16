import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CLASSES = [
    "Tomato_Early_Blight",
    "Tomato_Late_Blight",
    "Potato_Early_Blight",
    "Corn_Common_Rust",
    "Healthy_Leaf"
]

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_leaves")

def create_leaf_base(width=224, height=224, is_corn=False):
    """Generates a leaf shape image with realistic background noise."""
    # Background: soil brown or outdoor background
    bg_color = (random.randint(40, 90), random.randint(30, 70), random.randint(20, 50))
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Base leaf color (varying shades of green)
    leaf_green = (random.randint(30, 70), random.randint(120, 180), random.randint(30, 60))

    if is_corn:
        # Long elongated corn leaf
        points = [
            (width // 4, 10),
            (width * 3 // 4, 10),
            (width * 4 // 5, height - 10),
            (width // 5, height - 10)
        ]
        draw.polygon(points, fill=leaf_green)
        # Midrib line
        draw.line([(width // 2, 10), (width // 2, height - 10)], fill=(80, 190, 80), width=3)
    else:
        # Oval / compound leaf shape
        bbox = [width // 6, height // 6, width * 5 // 6, height * 5 // 6]
        draw.ellipse(bbox, fill=leaf_green)
        # Leaf stem and veins
        draw.line([(width // 2, height * 5 // 6), (width // 2, height - 5)], fill=(20, 100, 20), width=4)
        draw.line([(width // 2, height // 2), (width // 4, height // 3)], fill=(40, 140, 40), width=2)
        draw.line([(width // 2, height // 2), (width * 3 // 4, height // 3)], fill=(40, 140, 40), width=2)

    return img, draw

def add_early_blight_spots(img, count=5):
    """Early Blight: Dark brown concentric spots with yellow halo."""
    width, height = img.size
    draw = ImageDraw.Draw(img)
    for _ in range(count):
        cx = random.randint(width // 3, width * 2 // 3)
        cy = random.randint(height // 3, height * 2 // 3)
        radius = random.randint(12, 22)
        
        # Yellow chlorotic halo
        halo_bbox = [cx - radius - 6, cy - radius - 6, cx + radius + 6, cy + radius + 6]
        draw.ellipse(halo_bbox, fill=(200, 200, 40))
        
        # Brown necrotic spot with concentric rings
        spot_bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        draw.ellipse(spot_bbox, fill=(60, 35, 15))
        inner_bbox = [cx - radius // 2, cy - radius // 2, cx + radius // 2, cy + radius // 2]
        draw.ellipse(inner_bbox, fill=(35, 20, 10))

def add_late_blight_lesions(img, count=3):
    """Late Blight: Large water-soaked grayish brown dark lesions."""
    width, height = img.size
    draw = ImageDraw.Draw(img)
    for _ in range(count):
        cx = random.randint(width // 4, width * 3 // 4)
        cy = random.randint(height // 4, height * 3 // 4)
        rx = random.randint(20, 40)
        ry = random.randint(20, 45)
        
        # Pale pale green/yellow border
        border_bbox = [cx - rx - 4, cy - ry - 4, cx + rx + 4, cy + ry + 4]
        draw.ellipse(border_bbox, fill=(170, 180, 70))
        
        # Dark grayish-brown water-soaked lesion
        lesion_bbox = [cx - rx, cy - ry, cx + rx, cy + ry]
        draw.ellipse(lesion_bbox, fill=(45, 40, 35))

def add_rust_pustules(img, count=15):
    """Corn Common Rust: Small raised reddish-orange pustules."""
    width, height = img.size
    draw = ImageDraw.Draw(img)
    for _ in range(count):
        cx = random.randint(width // 3, width * 2 // 3)
        cy = random.randint(height // 6, height * 5 // 6)
        r = random.randint(4, 9)
        pustule_bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(pustule_bbox, fill=(210, 80, 20)) # Rusty orange

def generate_dataset(num_per_class=60):
    """Generates synthetic dataset for ML training."""
    print(f"Generating synthetic plant leaf dataset ({num_per_class} images/class)...")
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs(SAMPLE_DIR, exist_ok=True)

    for cls in CLASSES:
        cls_dir = os.path.join(DATASET_DIR, cls)
        os.makedirs(cls_dir, exist_ok=True)

        is_corn = "Corn" in cls
        for i in range(num_per_class):
            img, _ = create_leaf_base(is_corn=is_corn)
            
            if cls == "Tomato_Early_Blight" or cls == "Potato_Early_Blight":
                add_early_blight_spots(img, count=random.randint(3, 7))
            elif cls == "Tomato_Late_Blight":
                add_late_blight_lesions(img, count=random.randint(2, 5))
            elif cls == "Corn_Common_Rust":
                add_rust_pustules(img, count=random.randint(12, 25))
            elif cls == "Healthy_Leaf":
                pass # Clean leaf

            # Add light Gaussian blur and noise to simulate real camera blur
            if random.random() > 0.5:
                img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

            save_path = os.path.join(cls_dir, f"{cls}_{i+1:03d}.jpg")
            img.save(save_path)

    print("Dataset generation complete!")

    # Save 3 distinctive sample images in sample_leaves for backend testing
    sample_configs = [
        ("Tomato_Early_Blight", "test_leaf_tomato_early_blight.jpg", False, lambda img: add_early_blight_spots(img, 6)),
        ("Tomato_Late_Blight", "test_leaf_tomato_late_blight.jpg", False, lambda img: add_late_blight_lesions(img, 4)),
        ("Corn_Common_Rust", "test_leaf_corn_rust.jpg", True, lambda img: add_rust_pustules(img, 18)),
        ("Healthy_Leaf", "test_leaf_healthy.jpg", False, lambda img: None)
    ]

    for label, filename, is_corn, fn in sample_configs:
        img, _ = create_leaf_base(is_corn=is_corn)
        fn(img)
        sample_path = os.path.join(SAMPLE_DIR, filename)
        img.save(sample_path)
        print(f"Saved sample test image: {sample_path}")

if __name__ == "__main__":
    generate_dataset()
