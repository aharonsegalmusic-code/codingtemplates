# Project: Student Grade Averager

## Overview
Build a simple Python script that reads student data from a JSON file and prints a grade summary to the terminal.

## Files to Create
- `grade_averager.py` — the main script
- `students.json` — the data file
- `requirements.txt` — empty (stdlib only)

## What the Script Does
1. Opens `students.json` from the same folder
2. For each student, calculates their average grade across all subjects
3. Prints a report like this:

```
Alice    — average: 87.3
Bob      — average: 74.0
Carol    — average: 91.7
David    — no grades

Class average: 84.3
Top student: Carol (91.7)
```

## students.json Content
```json
[
  { "name": "Alice",  "grades": { "math": 90, "english": 85, "science": 87 } },
  { "name": "Bob",    "grades": { "math": 70, "english": 78, "science": 74 } },
  { "name": "Carol",  "grades": { "math": 95, "english": 88, "science": 92 } },
  { "name": "David",  "grades": {} }
]
```

## Requirements
- Python standard library only (no pip installs)
- Handle a student with no grades — print "no grades" for them
- Keep the code simple and easy to read
