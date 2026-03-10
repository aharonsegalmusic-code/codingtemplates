# Student Grade Averager

A simple Python script that reads student data from a JSON file and prints a formatted grade summary to the terminal.

## Data Flow

```
students.json  ->  grade_averager.py  ->  terminal output
```

## What It Does

1. Reads `students.json` from the same folder
2. Calculates each student's average grade across all their subjects
3. Prints each student's name and average (or "no grades" if they have none)
4. Prints the overall class average and the top student

## Example Output

```
Alice    — average: 87.3
Bob      — average: 74.0
Carol    — average: 91.7
David    — no grades

Class average: 84.3
Top student: Carol (91.7)
```

## Project Structure

```
project_1/
├── grade_averager.py   # main script
├── students.json       # input data
├── requirements.txt    # no external dependencies
├── dilemmas.md         # decisions made during generation
└── doc/
    ├── README.md       # this file
    ├── run.md          # how to run the project
    └── project_state.md
```

## Setup and Run

No installation required — uses Python standard library only.

```bash
python grade_averager.py
```

See `doc/run.md` for full setup instructions.
