#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
unset CLAUDECODE

cleanup() {
    echo "SESSION_ENDED" > "_session_state.txt"
}
trap cleanup EXIT

echo "STARTING" > "_session_state.txt"
echo ""
echo "[$(date +'%H:%M:%S')] Starting Claude Code..."
echo ""

claude --dangerously-skip-permissions --max-turns 200 \
  "Execute the full task described in your CLAUDE.md memory file. Complete everything now."
CLAUDE_EXIT=$?
echo $CLAUDE_EXIT > "_claude_exit.txt"
echo "INITIAL_DONE:$CLAUDE_EXIT" > "_session_state.txt"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Task complete  (exit $CLAUDE_EXIT)"
echo "  Terminal is open — type  claude --resume  to continue here"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Keep terminal open for direct Claude interaction
exec bash
