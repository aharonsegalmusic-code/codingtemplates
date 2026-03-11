# COMMUNICATE MODE — Requirements Clarification

**Project:** test_project
**Received:** 2026-03-11T09:05:10.539611+00:00
**Mode:** COMMUNICATE

---

## YOUR ONLY TASK

Read the instruction files below. Then write **one file**:
```
C:\Users\a0527\claude-pipeline-work\projects\test_project\9.template_max\projects\test_project\clarification.md
```

Create `C:\Users\a0527\claude-pipeline-work\projects\test_project\9.template_max\projects\test_project` first if it does not exist.

Use this exact format:

```markdown
# Clarification Questions for test_project

## [Topic Group — e.g. Architecture]

**Q1:** [Specific technical question]
> ANSWER:

**Q2:** [Another question]
> ANSWER:

## [Topic Group — e.g. Features]

**Q3:** [Question]
> ANSWER:
```

Rules for the questions:
- Group by topic (Architecture, Features, Data Model, Deployment, UI/UX, etc.)
- Be specific and technical — only ask what affects how you write the code
- Aim for 5–15 questions total
- Don't ask about obvious defaults (assume standard practices unless specified)

## AFTER WRITING clarification.md

```bash
git add -A
git commit -m "communicate: questions for test_project"
git push
```

Then **stop**. Do NOT write any code. Do NOT create any other files.

---

---

## INSTRUCTION FILES

### FLOW.md

```
# Test Flow — Hello World

**Open terminal at repo root, then:**
```bash
cd 9.template_max
```

**PC2:** start the orchestrator (leave running)
```bash
python start_generator.py
```

---

## 1. Communicate — Claude asks questions

Edit `run.py`:
```python
MODE    = "communicate"
PROJECT = "test_project"
```
```bash
python run.py
```
Wait for `✓ Done!`, then:
```bash
git pull
```
Open `projects/test_project/clarification.md`, fill in every `> ANSWER:` line, then push:
```bash
git add -A && git push
```

---

## 2. Code — Claude builds

Edit `run.py`:
```python
MODE = "code"
```
```bash
python run.py
```
Wait for `✓ Done!`, then:
```bash
git pull
```
Code is in `projects/test_project/`

---

## 3. Next feature — Communicate again

Add the new requirement to `projects/test_project/instructions.md`, then:

```python
MODE = "communicate"
```
```bash
python run.py
```
Fill in `clarification.md` answers → push → set `MODE = "code"` → run again.

---

## Expected output folder

```
projects/test_project/
├── main.py
├── requirements.txt
├── README.md
├── dilemmas.md
└── doc/
    └── project_state.md
```

```

### instructions.md

```
# i want to test the system before we start i know i want the data pipline but for not just give a hello world
regard the formats and rules and file requests but i want simple hello world code 
```
