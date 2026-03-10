# Dilemmas

## 1. Where to place README.md

**Dilemma:** The CRITICAL OPERATING RULES say "Include a README.md with clear setup and run instructions", while the permanent coding rules (section 15) say every project must have a `doc/README.md`. These two instructions point to different locations.

**Options considered:**
- Put README.md at the project root (satisfies the critical rule literally)
- Put README.md inside `doc/` folder (satisfies the permanent coding rules)
- Put README.md in both places

**Choice:** README.md is placed inside `doc/` and a short README.md is also placed at the project root pointing to `doc/README.md`.

**Why:** The permanent coding rules are explicit about `doc/README.md`. The root README serves as a pointer so anyone who opens the folder immediately knows where to look.

---

## 2. Apply fix.md immediately or separately

**Dilemma:** The project includes both `instructions.md` (build the project) and `fix.md` (add docstrings and comments). Since this is a NEW PROJECT, it is unclear whether to build first then patch, or build with all improvements from the start.

**Options considered:**
- Build the script without docstrings, then apply fix.md as a second pass
- Build the script with all docstrings and comments already included

**Choice:** Built the script with all docstrings and comments included from the start.

**Why:** Applying a fix on top of newly created code adds unnecessary steps. Since both instructions are available up front, building the final version directly is simpler and cleaner.

---

## 3. Architecture rules vs simple standalone script

**Dilemma:** The permanent coding rules describe a full multi-service backend architecture (docker-compose, shared/ folder, Kafka, Elasticsearch, etc.). The actual project is a simple standalone Python script with no external services.

**Options considered:**
- Apply all architecture rules (create docker-compose, shared/, services/ structure)
- Apply only the rules that are relevant to a single-script project

**Choice:** Applied only relevant rules (file docstrings, comment style, variable naming, doc/ folder, dilemmas.md, project_state.md). Skipped Docker, Kafka, Elasticsearch, shared/ folder, and service structure entirely.

**Why:** The instructions.md explicitly says "Python standard library only" and "no pip installs". The architecture rules are designed for multi-service backend systems. Forcing that structure onto a single stdlib script would violate the "keep it simple and educational" principle.
