"""
models/scripts/train_logo_cnn.py
Week 2 Deliverable: CNN Logo Classifier — Standalone Training Script
Tools: TensorFlow/Keras, OpenCV, NumPy, scikit-learn

Usage:
    python train_logo_cnn.py --data_dir data/logos/ --epochs 25
    python train_logo_cnn.py --demo   # Run with synthetic data
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    import cv2
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available — install with: pip install tensorflow")

IMG_SIZE    = (128, 128)
NUM_CLASSES = 8
INDUSTRIES  = ["Technology","Finance","Healthcare","Retail","Education","Fashion","Travel","Food & Beverage"]
MODEL_SAVE  = "models/logo_cnn.h5"
EMB_SAVE    = "models/logo_embeddings.npy"
LABEL_SAVE  = "models/logo_labels.npy"


def load_logo_dataset(data_dir: str):
    """Load logo images from data_dir/{industry}/*.png structure."""
    X, y = [], []
    for idx, industry in enumerate(INDUSTRIES):
        industry_dir = os.path.join(data_dir, industry.replace(" & ", "_").lower())
        if not os.path.exists(industry_dir):
            continue
        for fname in os.listdir(industry_dir):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                img = cv2.imread(os.path.join(industry_dir, fname))
                if img is None:
                    continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, IMG_SIZE)
                img = img / 255.0
                X.append(img)
                y.append(idx)
    return np.array(X, dtype="float32"), np.array(y)


def generate_synthetic_data(n: int = 600):
    """Synthetic data for demonstration when real dataset unavailable."""
    np.random.seed(42)
    X = np.random.rand(n, *IMG_SIZE, 3).astype("float32")
    y = np.random.randint(0, NUM_CLASSES, n)
    return X, y


def build_cnn(num_classes: int = NUM_CLASSES) -> "tf.keras.Model":
    """Build CNN architecture as specified in Week 2 brief."""
    model = Sequential([
        # Block 1
        Conv2D(32, (3, 3), activation="relu", padding="same", input_shape=(*IMG_SIZE, 3)),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        # Block 2
        Conv2D(64, (3, 3), activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        # Block 3
        Conv2D(128, (3, 3), activation="relu", padding="same"),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        # Classifier head
        Flatten(),
        Dense(256, activation="relu"),
        Dropout(0.4),
        Dense(num_classes, activation="softmax"),
    ], name="BrandMind_Logo_CNN")
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train(data_dir: str = None, epochs: int = 25, batch_size: int = 32, demo: bool = False):
    if not TF_AVAILABLE:
        print("TensorFlow required. Install: pip install tensorflow")
        return

    print("=" * 55)
    print("BrandMind AI — CNN Logo Classifier Training (Week 2)")
    print("=" * 55)

    # Load data
    if demo or not data_dir or not os.path.exists(data_dir or ""):
        print("Using synthetic data for demonstration...")
        X, y = generate_synthetic_data(600)
    else:
        print(f"Loading logos from: {data_dir}")
        X, y = load_logo_dataset(data_dir)
        if len(X) == 0:
            print("No images found — falling back to synthetic data.")
            X, y = generate_synthetic_data(600)

    y_cat = to_categorical(y, NUM_CLASSES)
    X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)
    print(f"Train: {X_train.shape} | Test: {X_test.shape}")

    # Augmentation
    datagen = ImageDataGenerator(
        rotation_range=20,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        zoom_range=0.15,
    )
    datagen.fit(X_train)

    # Build model
    model = build_cnn(NUM_CLASSES)
    model.summary()

    # Callbacks
    os.makedirs("models", exist_ok=True)
    callbacks = [
        EarlyStopping(patience=6, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_SAVE, save_best_only=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=3, verbose=1),
    ]

    # Train
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=batch_size),
        validation_data=(X_test, y_test),
        epochs=epochs,
        callbacks=callbacks,
        verbose=1,
    )

    # Evaluate
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nFinal Validation Accuracy: {acc * 100:.2f}%")

    # Training curves
    os.makedirs("outputs", exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(history.history["accuracy"], label="Train")
    axes[0].plot(history.history["val_accuracy"], label="Validation")
    axes[0].set_title("CNN Accuracy"); axes[0].legend()
    axes[1].plot(history.history["loss"], label="Train")
    axes[1].plot(history.history["val_loss"], label="Validation")
    axes[1].set_title("CNN Loss"); axes[1].legend()
    plt.tight_layout()
    plt.savefig("outputs/cnn_training_curves.png", dpi=150)
    plt.close()
    print("Saved: outputs/cnn_training_curves.png")

    # Extract embeddings
    embedding_model = Model(inputs=model.input, outputs=model.layers[-3].output)
    embeddings = embedding_model.predict(X_test, verbose=0)
    np.save(EMB_SAVE, embeddings)
    np.save(LABEL_SAVE, np.argmax(y_test, axis=1))
    print(f"Embeddings saved: {EMB_SAVE} {embeddings.shape}")

    # PCA visualisation
    pca = PCA(n_components=2)
    emb_2d = pca.fit_transform(embeddings)
    labels = np.argmax(y_test, axis=1)
    colors = plt.cm.Set1(np.linspace(0, 1, NUM_CLASSES))

    fig, ax = plt.subplots(figsize=(10, 6))
    for cls in range(NUM_CLASSES):
        mask = labels == cls
        if mask.sum() == 0:
            continue
        ax.scatter(emb_2d[mask, 0], emb_2d[mask, 1],
                   c=[colors[cls]], label=INDUSTRIES[cls], alpha=0.7, s=45,
                   edgecolors="white", linewidth=0.4)
    ax.set_title("PCA — Logo Embedding Clusters by Industry", fontsize=12, fontweight="bold")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    plt.savefig("outputs/logo_pca_clusters.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/logo_pca_clusters.png")
    print(f"\nModel saved: {MODEL_SAVE}")
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BrandMind CNN Logo Trainer (Week 2)")
    parser.add_argument("--data_dir", type=str, default=None, help="Logo image dataset directory")
    parser.add_argument("--epochs",   type=int, default=25,   help="Training epochs")
    parser.add_argument("--batch",    type=int, default=32,   help="Batch size")
    parser.add_argument("--demo",     action="store_true",    help="Run with synthetic data")
    args = parser.parse_args()
    train(data_dir=args.data_dir, epochs=args.epochs, batch_size=args.batch, demo=args.demo)
