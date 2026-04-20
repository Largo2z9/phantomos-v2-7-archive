#!/bin/sh
#
# PhantomOS workspace pre-commit hook
# Runs validate-all.py in strict mode. Blocks commit if HIGH or CRITICAL issues found.
#
# Install: `make install-hook` from workspace-template/ root
# Uninstall: `make uninstall-hook`
# Bypass (emergency only): `git commit --no-verify`

set -e

# Locate workspace-template/ relative to git root
GIT_ROOT=$(git rev-parse --show-toplevel)
SCRIPT="$GIT_ROOT/workspace-template/resources/scripts/validate-all.py"

# Fallback: maybe workspace-template IS the repo root
if [ ! -f "$SCRIPT" ]; then
    SCRIPT="$GIT_ROOT/resources/scripts/validate-all.py"
fi

if [ ! -f "$SCRIPT" ]; then
    echo "⚠ pre-commit: validate-all.py introuvable, hook skippé"
    exit 0
fi

echo "→ Validation workspace PhantomOS…"
if python3 "$SCRIPT" --strict; then
    echo "✓ Workspace clean, commit autorisé"
    exit 0
else
    echo ""
    echo "✗ Validation échouée. Commit bloqué."
    echo "  Fix les issues HIGH/CRITICAL ci-dessus, puis recommit."
    echo "  Bypass d'urgence : git commit --no-verify"
    exit 1
fi
