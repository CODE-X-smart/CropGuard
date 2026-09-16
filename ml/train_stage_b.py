import os
import time
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets, models
from sklearn.metrics import classification_report, confusion_matrix

CLASSES = [
    "Tomato_Early_Blight",
    "Tomato_Late_Blight",
    "Potato_Early_Blight",
    "Corn_Common_Rust",
    "Healthy_Leaf"
]

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "cropguard_mobilenetv3.pth")
METRICS_SAVE_PATH = os.path.join(os.path.dirname(__file__), "training_metrics.json")

def build_model(num_classes=5):
    """Builds a MobileNetV3-Small architecture for leaf disease classification."""
    try:
        # Load MobileNetV3 small architecture
        model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(in_features, num_classes)
    except Exception as e:
        print(f"Loading pretrained weights failed ({e}), creating model from scratch...")
        model = models.mobilenet_v3_small(weights=None, num_classes=num_classes)
    return model

def train_model():
    print("=== Starting Stage B (MobileNetV3 Leaf Disease CNN) Training ===")
    
    # Transforms for data augmentation and normalization
    transform_train = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    transform_val = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load full dataset
    full_dataset = datasets.ImageFolder(DATASET_DIR, transform=transform_train)
    class_to_idx = full_dataset.class_to_idx
    print(f"Dataset classes mapped: {class_to_idx}")

    # Split train/val
    total_size = len(full_dataset)
    val_size = int(0.2 * total_size)
    train_size = total_size - val_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    # Override val_dataset transform
    val_dataset.dataset.transform = transform_val

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

    # Initialize model, loss, optimizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    model = build_model(num_classes=len(CLASSES)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 5
    start_time = time.time()

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += torch.sum(preds == labels.data).item()
            total_train += labels.size(0)

        epoch_loss = running_loss / train_size
        epoch_acc = correct_train / total_train

        # Validation phase
        model.eval()
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                correct_val += torch.sum(preds == labels.data).item()
                total_val += labels.size(0)

        val_acc = correct_val / total_val
        print(f"Epoch [{epoch+1}/{epochs}] - Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc*100:.2f}% | Val Acc: {val_acc*100:.2f}%")

    training_duration = time.time() - start_time
    print(f"Training completed in {training_duration:.2f} seconds.")

    # Compute final evaluation metrics on validation set
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())

    # Generate classification report and confusion matrix
    target_names = [CLASSES[idx] for idx in range(len(CLASSES))]
    report = classification_report(all_targets, all_preds, target_names=target_names, output_dict=True)
    conf_mat = confusion_matrix(all_targets, all_preds).tolist()

    print("\n=== Final Validation Classification Report ===")
    print(classification_report(all_targets, all_preds, target_names=target_names))

    # Save model weights
    torch.save({
        'model_state_dict': model.state_dict(),
        'classes': CLASSES,
        'class_to_idx': class_to_idx
    }, MODEL_SAVE_PATH)
    print(f"Saved trained PyTorch model to: {MODEL_SAVE_PATH}")

    # Save metrics JSON for verification report
    metrics_payload = {
        'total_samples': total_size,
        'train_samples': train_size,
        'val_samples': val_size,
        'epochs': epochs,
        'final_val_acc': float(val_acc),
        'classification_report': report,
        'confusion_matrix': conf_mat,
        'training_duration_seconds': float(training_duration)
    }

    with open(METRICS_SAVE_PATH, 'w') as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"Saved training metrics report to: {METRICS_SAVE_PATH}")

if __name__ == "__main__":
    train_model()
