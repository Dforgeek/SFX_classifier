# 🎧 SFX Classifier — *Sort your sound palette in one command!*

> A lightning‑fast CLI that sifts through a folder of miscellaneous audio samples and neatly places them into four musical drawers:
> **Drums · Synths · Voice · Water**.

---

## ✨ Why you’ll love it

| 🔑 Feature                        | 🚀 Benefit                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------- |
| **📂 One‑liner sorting**          | Point to any directory — even thousands of files deep — and watch it organise itself. |
| **🧠 Trained CNN under the hood** | Uses your own `SampleClassifier` weights (or ours) for studio‑grade accuracy.         |
| **⚡ GPU optional**                | Harness CUDA in a single flag, or run comfortably on CPU.                             |
| **🤝 Non‑destructive mode**       | `--copy` keeps your originals untouched; perfect for archival libraries.              |
| **🔌 Minimal dependencies**       | `torch`, `librosa`, `numpy`, `tqdm`, `soundfile`. That’s it.                          |
| **🛠 Easy to extend**             | Swap weights, add new classes, or embed in a bigger pipeline.                         |

---

## 🖇️ Installation

```bash
# Create & activate a clean environment (optional but recommended)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install torch librosa numpy tqdm soundfile
```

Clone or drop `classify_samples.py` + your weight file (`audio_classifier_cnn.pth`) into your project folder.

---

## 🚀 Quick Start

```bash
python classify_samples.py /path/to/unsorted_samples
```

**Common flags**

```bash
--weights  path/to/weights.pth   # use alternative weights file
--cuda                          # infer on the first available GPU
--copy                          # copy instead of move (keeps originals)
```

Full example:

```bash
python classify_samples.py ./previews --weights audio_classifier_cnn.pth --cuda --copy
```

After completion you’ll see:

```
Classifying: 100%|█████████████| 1472/1472 [01:12<00:00, 20.3it/s]
kick_018.wav          → drum_samples
splash_large.flac     → water_samples
...

Summary
────────
drum_samples   : 519
synth_samples  : 411
voice_samples  : 286
water_samples  : 256
```

…and four freshly minted sub‑folders inside your target directory.

---

## 🔍 How it works

1. **Pre‑processing** — stereo→mono, resample to 24 kHz, mel‑spectrogram (128 mels, 50 fps), zero‑pad/truncate to \~13 s.
2. **CNN inference** — architecture copied from the notebook you trained: two conv blocks → adaptive‑avg‑pool → dense.
3. **Hard max** — highest logit dictates the class.
4. **File IO** — sorted with `shutil.move` *(or `copy`)*; already‑sorted files are skipped.

> Swap in your own spectrogram routine or model by editing `preprocess()` and `SampleClassifier`.

---

## 🧩 Extending & Embedding

* **Add classes:** list new folder names in `classes`, adjust `num_classes` in the model, retrain & save new weights.
* **Batch scripts:** integrate into Ableton/FL Studio prep, run from CI, or wrap in a PyQt GUI — it’s just Python.
* **Dataset building:** pass `--copy` and keep originals tidy while you curate training data.

---

## 🤗 Contributing

Pull requests are welcome!  Please open an issue for feature requests or bugs.

1. Fork the repo
2. Create a feature branch: `git checkout -b cool_feature`
3. Commit changes & push
4. Open a PR 🎉

---

## 📝 License

Released under the **MIT License** — free to use, modify, and distribute, with attribution.

---

## 🙏 Credits

Built upon the brilliant open‑source ecosystems of **PyTorch**, **librosa**, **NumPy**, and **Freesound**.

> May your sample library always be organised and your creativity unblocked!
