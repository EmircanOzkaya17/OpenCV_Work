<p align="center">
  <img src="assets/logo.png" alt="OpenCv Works" width="250">
</p>

# OpenCv Works: Comprehensive Image Processing Applications

This project serves as a comprehensive reference repository for **fundamental and intermediate image processing applications** implemented using the **OpenCV** library.

The primary goal of this project is to provide practical and easy-to-understand code examples for those new to the field of **Computer Vision**.

### 📚 Table of Contents

1. [✨ Core Topics Covered](#-core-topics-covered)
2. [⚙️ Project Structure and Files](#-project-structure-and-files)
3. [🚀 Installation and Setup](#-installation-and-setup)
4. [📝 License](#-license)

---

### ✨ Core Topics Covered

The main topics and practical demonstrations covered within this repository include:

* **Basic Image Operations:** Fundamental operations such as reading, resizing, combining (concatenation), and saving images.
* **Simple Drawing:** Adding shapes (lines, circles, rectangles) and text overlays onto images.
* **Color Channels:** Working with different color spaces (BGR, HSV, Grayscale), and performing channel splitting and merging operations.
* **Image Quality Enhancement:** Sharpening algorithms and various Blurring techniques.
* **Morphological Operations:** Shape-based filtering methods like Erosion, Dilation, Opening, and Closing.

---

## ⚙️ Project Structure and Files

The repository is organized into specific example folders, each focusing on a different aspect of image processing.

```text
OpenCV_Work/
├── assets/
│   ├── logo.png               # Project logo
│   ├── albert.jpg             # Sample image
│   ├── petersburg.jpg         # Sample image
│   ├── cloud.jpg              # Sample image
│   └── swartz.jpg             # Sample image
├── src/
│   ├── Example_1/             # Basics: Reading, Saving, Drawing
│   │   ├── A Small Application/
│   │   ├── basic drawings.py
│   │   └── image_read_show_save.py
│   ├── Example_2/             # Manipulations: Color, Crop, Resize, Rotation
│   │   ├── A Small Application/
│   │   ├── color_spaces.py
│   │   ├── collage.py
│   │   └── ...
│   └── Example_3/             # Enhancements: Blur, Sharpening, Morphology
│       ├── blur__.py
│       ├── morphology__.py
│       └── sharp.py
├── requirements.txt           # List of dependencies
└── README.md                  # Project documentation

---

## 🚀 Installation and Setup

Follow these steps to set up the project locally on your machine.

### 1. Clone the Repository
Open your terminal and clone the repository:

```bash
git clone [https://github.com/EmircanOzkaya17/OpenCV_Work.git](https://github.com/EmircanOzkaya17/OpenCV_Work.git)
cd OpenCV_Work

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python "src/Example_1/image_read_show_save.py"