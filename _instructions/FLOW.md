# Test Flow — Hello World

---

## Before you start

**PC2:** run the orchestrator (leave it running)
```bash
cd docs/9.template_max

python start_generator.py
```

**PC1:** make sure `run.py` points to this project
```python
PROJECT = "test_project"
```

---

## Option A — Skip communicate, go straight to code

For something this simple there's nothing to clarify.

**1. Edit `run.py`:**
```python
MODE    = "code"
PROJECT = "test_project"
```

**2. Run:**
```bash
python run.py
```

**3. Wait for:** `✓ Done!` in the terminal, then:
```bash
git pull
```

**4. Your code is in:** `projects/test_project/`

---

## Option B — Full communicate → code flow

### Step 1: Communicate (Claude asks questions)

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
Open `projects/test_project/clarification.md`, fill in the `> ANSWER:` lines, then push:
```bash
git add -A && git push
```

---

### Step 2: Code (Claude builds)

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

**Done.** Code is in `projects/test_project/`

---

## What to expect in the output folder

```
projects/test_project/
├── main.py              ← the hello world code
├── requirements.txt
├── README.md
├── dilemmas.md
└── doc/
    └── project_state.md
```
