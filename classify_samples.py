"""
CLI-утилита для сортировки музыкальных семплов.
Пример:  python classify_samples.py ./unsorted --weights audio_classifier_cnn.pth
"""

import argparse, os, shutil, glob
import numpy as np
import librosa, torch
import torch.nn as nn
from tqdm import tqdm


class SampleClassifier(nn.Module):
    """CNN-классификатор на мел-спектрограммах (точь-в-точь, как в ноутбуке)."""
    def __init__(self, num_classes: int = 4):
        super().__init__()
        self.conv_block = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))
        self.fc = nn.Sequential(
            nn.Linear(32 * 4 * 4, 128), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.adaptive_pool(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


def preprocess(path, sr=24_000, n_mels=128, n_fft=2048,
               hop=512, max_frames=640):
    """Готовим тензор формы (1, 1, n_mels, max_frames)."""
    y, _ = librosa.load(path, sr=sr, mono=False)
    if y.ndim == 2:                  # стерео → моно
        y = y.mean(axis=0)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop, n_mels=n_mels
    )
    mel = librosa.power_to_db(mel, ref=np.max)
    # выравниваем длину по времени
    if mel.shape[1] > max_frames:
        mel = mel[:, :max_frames]
    elif mel.shape[1] < max_frames:
        pad = max_frames - mel.shape[1]
        mel = np.pad(mel, ((0, 0), (0, pad)), mode="constant")
    return torch.tensor(mel, dtype=torch.float32).unsqueeze(0).unsqueeze(0)


@torch.no_grad()
def classify_folder(folder, weights="audio_classifier_cnn.pth",
                    device="cpu", move=True):
    classes = ["drum_samples", "synth_samples", "voice_samples", "water_samples"]
    model = SampleClassifier().to(device)
    model.load_state_dict(torch.load(weights, map_location=device))
    model.eval()

    for c in classes:
        os.makedirs(os.path.join(folder, c), exist_ok=True)

    exts = {".wav", ".mp3", ".flac", ".ogg", ".aiff", ".aif", ".m4a"}
    counters = {c: 0 for c in classes}

    for file in tqdm(sorted(glob.glob(os.path.join(folder, "**", "*"), recursive=True)),
                     desc="Classifying"):
        if (not os.path.isfile(file)
                or os.path.splitext(file)[1].lower() not in exts):
            continue
        # пропускаем уже отсортированное
        if os.path.basename(os.path.dirname(file)) in classes:
            continue

        x = preprocess(file).to(device)
        pred = model(x).argmax(1).item()
        dst = os.path.join(folder, classes[pred], os.path.basename(file))
        if move:
            shutil.move(file, dst)
        else:
            shutil.copy(file, dst)
        counters[classes[pred]] += 1
        print(f"{os.path.relpath(file, folder)} → {classes[pred]}")

    print("\nИтого:")
    for c, n in counters.items():
        print(f"{c:<15}: {n}")


def main():
    print("jsdjds")
    parser = argparse.ArgumentParser(
        description="Классификация и сортировка музыкальных семплов")
    parser.add_argument("folder", help="Папка с несортированными файлами")
    parser.add_argument("--weights", default="audio_classifier_cnn.pth",
                        help="Путь к файлу весов модели (.pth)")
    parser.add_argument("--cuda", action="store_true",
                        help="Использовать GPU, если доступно")
    parser.add_argument("--copy", action="store_true",
                        help="Копировать, а не перемещать файлы")
    args = parser.parse_args()

    device = ("cuda" if args.cuda and torch.cuda.is_available() else "cpu")
    classify_folder(args.folder, args.weights, device, move=not args.copy)


if __name__ == "__main__":
    main()
