# ISIMS Semester 2 Computer Science Projects 🎓

Welcome to my academic repository showcasing the practical programming and web development projects I completed during my second semester pursuing a Licence degree in Computer Science at the Higher Institute of Computer Science and Multimedia of Sfax (ISIMS). 

This repository documents my hands-on experience with Python scripting, algorithmic logic, and responsive web styling.

---

## 📂 Repository Structure & Project Breakdown

### 🐍 Python Projects
* `📁 project1-simple-calculator/`
    * A clean, functional arithmetic calculator built to practice foundational programming logic, conditional execution, and user input handling in Python.
* `📁 project2-word-count-tfidf/`
    * A text analysis tool that calculates total word counts and computes **TF-IDF (Term Frequency-Inverse Document Frequency)** metrics to evaluate word importance within documents. 
* `📁 project3-gestion-fichier/`
    * An application designed for structured file management (*application de gestion de fichiers*), focusing on file I/O operations, directory handling, and data persistence in Python.

### 🌐 Web Development Projects
* `📁 game-event-website/`
    * A fully responsive, themed landing website for a gaming event. Built from scratch using semantic **HTML5** for structure and custom **CSS3** for layout design, animations, and modern UI elements.

---

## 🛠️ Core Technologies & Concepts Applied

* **Languages & Styling:** Python , HTML5, CSS3 
* **Text Analysis & Data Logic:** Text parsing, tokenization, and mathematical modeling (TF-IDF algorithm implementation).
* **System Operations:** File manipulation, reading/writing local data streams, and structural organization.
* **Frontend Design:** Responsive web layouts, flexbox/grid architecture, and clean UI/UX principles.

---

## 🚀 Key Highlights

### TF-IDF & Word Analyzer (Python)
Instead of just counting words, this script applies basic natural language processing logic to analyze text data and determine the statistical relevance of terms across multiple documents.

### Gaming Event Platform (HTML & CSS)
A project focused on translating a visual theme into a clean web interface , ensuring proper alignment, readable typography, and smooth layout transitions without relying on heavy frameworks.

---

## 🚀 How to Run the Python Code Locally

Follow these steps to set up your environment, install the necessary dependencies, and run the applications on your local machine.

### 📋 Prerequisites
Before you begin, ensure you have the following installed:
* **Python 3.x**
* **pip** (Python package installer)
* **git** (optional, to clone the repository)

---

### 🛠️ Step-by-Step Setup

#### 1. Clone or Download the Repository
Open your terminal (or PowerShell), clone the repository, and navigate into the root directory:
```bash
git clone https://github.com/abdelaziz5/isims-unv-first-year.git
cd isims-semester2-projects
```
*(Alternatively, you can download the project as a ZIP file from GitHub, extract it, and open your terminal inside that main folder).*

#### 2. Create and Activate a Virtual Environment (Recommended)
To keep your global Python installation clean, set up an isolated virtual environment:

* **On Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate.ps1
  ```
* **On Windows (Command Prompt / CMD):**
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```

*Once activated, you will see `(.venv)` appear at the very beginning of your terminal line.*

#### 3. Install Dependencies from requirements.txt
Run this exact command while your virtual environment is active. It tells pip to read your `requirements.txt` file from the root folder and automatically download and install all the necessary libraries (like `PyQt5`) for you:
```bash
pip install -r requirements.txt
```

#### 4. Navigate to a Project and Run It
Now that your environment is fully configured, navigate into the specific project folder you want to view and execute the script:

* **Example: Running the Simple Calculator**
  ```bash
  cd python/01-simple-calculator
  python main.py
  ```

* **Example: Running the Word Count & TF-IDF Tool**
  ```bash
  cd python/02-word-count-tfidf
  python main.py
  ```

---

## 👤 Contact & Connect
* **Name:** Abdelaziz Masmoudi 
* **LinkedIn:** [Click Here](www.linkedin.com/in/abdelaziz-masmoudi-me)
* **Institution:** Higher Institute of Computer Science and Multimedia of Sfax (ISIMS)
