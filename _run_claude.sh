#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
unset CLAUDECODE

# Write SESSION_ENDED whenever this script exits (window closed, Ctrl+C, etc.)
cleanup() {
    echo "SESSION_ENDED" > "_session_state.txt"
}
trap cleanup EXIT

echo "STARTING" > "_session_state.txt"

# ── Initial generation ────────────────────────────────────────────
echo ""
echo "[$(date +'%H:%M:%S')] Starting initial generation..."
echo ""
claude --dangerously-skip-permissions --max-turns 100 \
  "Execute the full task described in your CLAUDE.md memory file. Complete everything now."
INITIAL_EXIT=$?
echo $INITIAL_EXIT > "_claude_exit.txt"
echo "INITIAL_DONE:$INITIAL_EXIT" > "_session_state.txt"

echo ""
echo "══════════════════════════════════════════════════════"
echo "  Generation complete  (exit code: $INITIAL_EXIT)"
echo "  SESSION IS ACTIVE — watching for fix requests"
echo "  Close this window to end the session."
echo "══════════════════════════════════════════════════════"
echo ""

# ── Fix polling loop ──────────────────────────────────────────────
while true; do
    if [ -f "_pending_fix.md" ]; then
        echo "[$(date +'%H:%M:%S')] Fix received — applying..."
        echo ""
        FIX=$(cat "_pending_fix.md")
        rm -f "_pending_fix.md"
        echo "PROCESSING_FIX" > "_session_state.txt"

        claude --dangerously-skip-permissions \
          "A fix has been requested for this project.

First read all existing project files to understand the current state, then apply exactly what is described below — nothing more.

--- FIX INSTRUCTIONS ---
${FIX}
--- END FIX INSTRUCTIONS ---

When done:
1. git add -A
2. git commit -m 'fix: [brief description]'
3. git push
Do NOT create complete.md."

        FIX_EXIT=$?
        echo "FIX_DONE:$FIX_EXIT" > "_session_state.txt"
        echo ""
        echo "[$(date +'%H:%M:%S')] Fix complete (exit $FIX_EXIT). Watching for next fix..."
        echo ""
    fi
    sleep 10
done
