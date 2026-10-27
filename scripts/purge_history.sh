#!/usr/bin/env bash
# Purge committed secrets (.env.prod, .env.backup, .env.test) from the whole git history.
#
# DESTRUCTIVE once pushed: this rewrites every commit hash on every branch.
# By default it only works on a throwaway mirror clone, writes a backup bundle and
# verifies the result. Nothing is pushed unless you pass --push.
#
# Usage:
#   scripts/purge_history.sh                # rewrite + verify a local mirror, no push
#   scripts/purge_history.sh --push         # same, then force-push branches and tags
#
# Environment:
#   REPO_URL      repository to clean (default: this checkout's `origin`)
#   WORKDIR       where the mirror and backup go (default: ./history-purge)
#   SECRET_FILE   optional file with one secret value per line (SECRET_KEY, DB_PASSWORD...).
#                 After the rewrite, the script fails if any value is still in history.
#                 Never commit this file.
#
# Requirements: git, git-filter-repo (pip install git-filter-repo).
#
# BEFORE running: rotate the exposed secrets. Rewriting history does not make them safe,
# because forks, clones and GitHub's cached views of old commits keep them.

set -euo pipefail

PATHS_TO_REMOVE=(.env.prod .env.backup .env.test)
PUSH=0
[[ "${1:-}" == "--push" ]] && PUSH=1

REPO_URL="${REPO_URL:-$(git remote get-url origin)}"
WORKDIR="${WORKDIR:-$PWD/history-purge}"
MIRROR="$WORKDIR/mirror.git"
BACKUP="$WORKDIR/backup-$(date -u +%Y%m%dT%H%M%SZ).bundle"

command -v git-filter-repo >/dev/null || { echo "git-filter-repo not found: pip install git-filter-repo" >&2; exit 1; }
[[ -e "$MIRROR" ]] && { echo "$MIRROR already exists; remove it or set WORKDIR" >&2; exit 1; }
mkdir -p "$WORKDIR"

echo "==> Cloning full history of $REPO_URL"
git clone --mirror "$REPO_URL" "$MIRROR"
cd "$MIRROR"

echo "==> Writing backup bundle: $BACKUP"
git bundle create "$BACKUP" --all

echo "==> Files to purge and the commits that contain them"
for p in "${PATHS_TO_REMOVE[@]}"; do
  echo "  $p: $(git log --all --oneline -- "$p" | wc -l) commit(s)"
done

echo "==> Rewriting history"
args=(--invert-paths)
for p in "${PATHS_TO_REMOVE[@]}"; do args+=(--path "$p"); done
git filter-repo "${args[@]}" --force
# filter-repo removes the origin remote as a safety measure; restore it for the push step.
git remote add origin "$REPO_URL"

echo "==> Verifying"
fail=0
for p in "${PATHS_TO_REMOVE[@]}"; do
  if [[ -n "$(git log --all --oneline -- "$p")" ]]; then echo "  STILL PRESENT: $p"; fail=1; fi
done
if [[ -n "${SECRET_FILE:-}" ]]; then
  while IFS= read -r secret; do
    [[ -z "$secret" ]] && continue
    if git grep -qF -- "$secret" $(git rev-list --all) 2>/dev/null; then
      echo "  SECRET STILL IN HISTORY (a line of $SECRET_FILE matches)"; fail=1
    fi
  done < "$SECRET_FILE"
fi
[[ $fail -eq 0 ]] || { echo "Verification failed; nothing was pushed." >&2; exit 1; }
echo "  OK: purged paths no longer appear in any commit"

if [[ $PUSH -eq 0 ]]; then
  cat <<EOF

Dry run finished. Rewritten mirror: $MIRROR
Backup of the original history:     $BACKUP

To publish (this REPLACES history on the remote), either re-run with a fresh WORKDIR and --push,
or push this already-verified mirror yourself:
  cd $MIRROR
  git push --force origin 'refs/heads/*' 'refs/tags/*'
EOF
  exit 0
fi

echo "==> Force-pushing rewritten branches and tags to $REPO_URL"
git push --force origin 'refs/heads/*' 'refs/tags/*'

cat <<EOF

Done. Next steps:
  1. Everyone with a clone must re-clone (or 'git fetch && git reset --hard origin/main').
  2. Open PRs and forks still hold the old commits. Close open PRs and ask fork owners to delete forks.
  3. GitHub keeps old commits reachable by hash (and refs/pull/*) for a while. Ask GitHub Support
     to run garbage collection and remove cached views if the secrets were ever live.
  4. Confirm the secrets listed in .env.prod were rotated.
EOF
