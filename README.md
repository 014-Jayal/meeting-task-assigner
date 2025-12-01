# 🎙️ Automatic Meeting Task Assigner

A Python-based automation tool that processes meeting audio recordings, identifies actionable tasks from conversations, and intelligently assigns them to team members based on their roles and skill sets.

**Submitted by:** Jayal Shah  
**Assessment for:** KriraAI Technical Assessment

---

## 📖 Project Overview

### Problem Statement
In real-world team meetings, identifying actionable items and assigning responsibility is a manual and error-prone process. Important tasks may be missed, misassigned, or forgotten entirely.

### Solution
This project automates the workflow by:

- 🗣️ Converting meeting audio into text using Speech-to-Text
- ✍️ Extracting actionable task statements from natural language
- 👤 Identifying responsible team members either by direct naming or skill matching
- ⏰ Detecting deadlines automatically
- 🚨 Recognizing priority levels from conversation
- 📊 Exporting structured task records into a CSV report

The result is an **automated meeting assistant** that improves accountability and productivity.

---

## 🛠️ Technical Architecture

The solution strictly follows the assessment constraints:

### Speech-to-Text
- Library: `SpeechRecognition`
- Engine: Google Web Speech API (only external service used)

### Natural Language Processing
- NLP Engine: spaCy (`en_core_web_sm` model)
- Custom Rule-based Logic:
  - Task detection via action verbs
  - Name detection using Named Entity Recognition
  - Deadline detection via DATE entities
  - Priority inference using keywords

### Data Handling
- Team skills database → JSON
- Task output report → CSV

---

## 📂 Project Structure

```
meeting_assigner/
│
├── data/
│   ├── input_audio.wav       # Meeting recording (input file)
│   └── team_members.json     # Team skills & roles database
│
├── src/
│   ├── main.py               # Application entry point
│   ├── transcriber.py        # Converts audio to text
│   └── processor.py          # NLP & task assignment engine
│
├── output/
│   └── task_assignments.csv  # Final generated report
│
└── requirements.txt          # Python dependencies
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or above
- Internet connection (for Google Speech API)
- OS: Windows / Linux / macOS

---

### 1. Clone the Repository

```
git clone <YOUR_GITHUB_REPO_LINK_HERE>
cd meeting_assigner
```

---

### 2. Create Virtual Environment

#### Windows
```
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## ▶️ Usage Guide

### Step 1: Prepare Input Audio
Place your meeting recording inside the `data/` directory and rename it as:

```
input_audio.wav
```

---

### Step 2: Run the Program

```
python src/main.py
```

---

### Step 3: View Results

- Transcribed meeting text is displayed on the console
- A structured task table is printed
- A CSV file is saved to:

```
output/task_assignments.csv
```

---

## 🧠 Core Logic Pipeline

### 1. Preprocessing & Sentence Segmentation
Cleans transcription output and intelligently splits sentences even when punctuation is missing.

### 2. Action Detection
Searches for action verbs:

```
fix, implement, update, design, build, test, deploy, review, write
```

Only actionable statements are extracted.

### 3. Entity & Metadata Extraction

#### ✅ Deadlines
- Tomorrow
- Friday
- 20th June
- Next Week

Handled via spaCy DATE entities.

#### ✅ Priority Detection
Keyword Based Scoring:

- urgent
- critical
- high priority
- asap

---

### 4. Smart Assignment Strategy

**Priority Order:**

1. **Explicit Mentions**  
   Example:
   "Sakshi, please fix the login bug"

2. **Skill Matching**  
   Example:
   "The API performance is slow" → Backend Engineer

The system scans task keywords against skill mappings in `team_members.json`.

---

## 📊 Sample Output

### Input Audio Context

```
"Sakshi, we need someone to fix the critical login bug..."
"Mohit, the database performance issue needs attention by Friday"
```

### Generated Output (CSV Preview)

| Description | Assignee | Priority | Deadline | Reason |  
|-------------|----------|----------|----------|--------|  
| Fix login bug | Sakshi | High | Today | Explicit name |  
| Database issue | Mohit | High | Friday | Skill match |  

---

## 🎥 Demo

Demo video link will be added here.

---

## ✅ Compliance Statement

This project adheres fully to the assessment constraints:

- ✅ No GPT / Gemini / LLM APIs used
- ✅ Only Google Speech API for transcription
- ✅ All logic implemented with spaCy + Python heuristics

---

## 🙌 Acknowledgements

- spaCy
- Python SpeechRecognition
- Open Source Community

---

## 📬 Contact

For queries or feedback:

**Jayal Shah**  
Email: jayalshah04@gmail.com

