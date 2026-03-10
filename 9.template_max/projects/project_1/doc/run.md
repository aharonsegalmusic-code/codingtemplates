# How to Run

## Local Setup

This project uses Python standard library only — no pip installs are needed.

### 1. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

### 2. Activate the virtual environment

On Windows with Git Bash:

```bash
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The requirements file is empty — this step has no effect but is included for consistency.

### 4. Run the script

```bash
python grade_averager.py
```

### Expected output

```
Alice    — average: 87.3
Bob      — average: 74.0
Carol    — average: 91.7
David    — no grades

Class average: 84.3
Top student: Carol (91.7)
```

## Notes

- The script reads `students.json` from the same folder automatically
- No internet connection, no Docker, no services required
- Works with Python 3.6 and above
