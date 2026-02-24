# Manu's Recipe Exploration (Recipe Finder)

**Recipe Finder** is an advanced Computer Vision and Natural Language Processing application designed to solve the age-old question: *"What is that, and how do I make it?"* 

By simply uploading a photo of a dish, this application utilizes deep learning to identify the food, predict the required ingredients, and automatically generate a step-by-step cooking recipe. Built with PyTorch and Flask, Recipe Finder bridges the gap between culinary inspiration and actual cooking by turning visual food experiences into actionable recipes.

![Homepage Light Mode](screenshots/homepage%20(White%20mode).png)
![Homepage Dark Mode](screenshots/Homepage%20(dark).png)

## ✨ Features
1. **AI Recipe Generation**: Uses a PyTorch-based Computer Vision/NLP model to extract ingredients and instructions from a single image.
2. **Food Image Validation**: Integrates a lightweight ResNet18 classifier to automatically reject non-food images before wasting resources on generation!
3. **Optimized AI Engine**: Includes global model caching. The huge PyTorch models only load into memory *once* on boot, making every subsequent upload lightning-fast.
4. **Beautiful Modern UI**: Features a sleek Glassmorphism design, centralized flex-box layout, smooth micro-animations, and a fully functional Dark / Light mode toggle that remembers your preference!

---

![Recipe Dark](screenshots/Chocolate%20cake%20recipe%20(Dark%20mode).png)
![Non food rejection](screenshots/Avengers%20(white%20mode).png)

---

## 🚀 How to Run Locally (Perfect Tutorial)

Follow these steps exactly to run the application securely and smoothly on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.8+** installed. You will also need `pip` to install the requirements.

### 2. Clone the Repository
```bash
git clone https://github.com/HADESOO7/Recipe-Finder.git
cd Recipe-Finder
```
*(If you are running Manu's customized version, just open your modified project folder in your terminal!)*

### 3. Create a Virtual Environment (Highly Recommended)
Creating a virtual environment ensures that the heavy PyTorch and Flask dependencies won't conflict with other Python tools on your computer.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: If the `requirements.txt` strictly pins an old PyTorch version that fails to install, simply run `pip install torch torchvision flask werkzeug pillow` to fetch the latest viable versions).*

### 5. Ensure the AI Model Data is Present
The application inherently relies on three massive pre-trained files that must be placed inside the `Foodimg2Ing/data/` folder:
- `ingr_vocab.pkl` (Ingredient Vocab)
- `instr_vocab.pkl` (Instruction Vocab)
- `modelbest.ckpt` (The core Deep Learning model checkpoint)

*If you do not have these files, the app will crash instantly on the first upload.*

### 6. Start the Server
Finally, run the Flask backend:
```bash
cd Foodimg2Ing
python run.py
```
Open your web browser and go to: `http://127.0.0.1:5000`

---

## 🛠️ Common Errors & How to Fix Them

### 🛑 1. Memory Crash / App Freezes Completely / Device BSOD
**The Cause:** Deep Learning models require a large amount of system RAM to load. The `modelbest.ckpt` and the `ResNet18` models are loaded simultaneously into memory.
**The Fix:** Make sure your PC has at least 8GB to 16GB of Free RAM. Close unnecessary Chrome tabs or heavy applications before booting the server!

### 🛑 2. Missing Files Error (`FileNotFoundError: [Errno 2] No such file or directory: 'data/modelbest.ckpt'`)
**The Cause:** The Python script is trying to load the AI model but you haven't put it in the correct folder, or you are running the `run.py` script from the wrong directory.
**The Fix:** Always run the application from inside the `Foodimg2Ing` directory, not the outer wrapper folder. Double check that `Foodimg2Ing/data/modelbest.ckpt` actually exists on your hard drive.

### 🛑 3. Port Blocking (`OSError: [WinError 10048] Only one usage of each socket address is permitted`)
**The Cause:** Another application on your computer, or an old instance of this python app that didn't shut down correctly, is already hogging Port `5000`.
**The Fix:** Open `Foodimg2Ing/run.py` in a text editor. Change the last line from `app.run(debug=True)` to `app.run(debug=True, port=8000)`. Then access the app at `http://127.0.0.1:8000`.

### 🛑 4. Non-Food Images Are Giving "IndexError" or "KeyError"
**The Cause:** If a user uploads a completely random image (like a car or a person), the original recipe generator hallucinates and breaks trying to index non-existent food words.
**The Fix:** This has actually been **FIXED** in Manu's custom version! The updated application routes all images through a ResNet18 classifier first to verify it's food. If it fails, the UI gracefully tells the user `Not a food image!`.

### 🛑 5. Outdated Dependencies Failing Build (e.g., `Failed building wheel for X`)
**The Cause:** The original `requirements.txt` might contain extremely outdated versions of `tensorflow` or `keras` that don't compile on Python 3.10+.
**The Fix:** You don't actually need TensorFlow if you are using the pure PyTorch execution path! Remove `tensorflow` and `keras` from your `requirements.txt` and just use `torch` and `torchvision`.
