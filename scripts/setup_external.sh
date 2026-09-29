#!/usr/bin/env bash
# Fetch Schesch et al.'s evaluation harness (code + committed results) at a pinned commit.
# Pin verified 2026-09-29: HEAD of main was 9238a737 (2025-01-27). Update the pin deliberately.
set -euo pipefail
PIN=9238a737f65f765bbfb9cbd10c8796f77304f198
DEST=external/AST-Merging-Evaluation
mkdir -p external
if [ ! -d "$DEST/.git" ]; then
  git clone https://github.com/benedikt-schesch/AST-Merging-Evaluation.git "$DEST"
fi
git -C "$DEST" fetch --all --quiet
git -C "$DEST" checkout "$PIN"
echo "Harness at $(git -C "$DEST" rev-parse --short HEAD)"
echo
echo "Committed results you need for step 1 (no Java required):"
ls -la "$DEST/results/combined/result_adjusted.csv" "$DEST/input_data/repos_combined.csv"
cat <<'MSG'

NOT downloaded automatically (large). Only fetch when you need to re-run tools:
  Zenodo record 10.5281/zenodo.13366866 (v3 when checked; a newer version exists -- check /latest)
    cache_without_logs.tar.gz  52.6 MB  md5 ca903aac57eda740ea7aa25e05263e10
    cache.tar                   6.6 GB  md5 9983b6cea9fad9b7512586a6c1b84a04   (84 GB uncompressed per harness README)
  https://zenodo.org/records/13366866
MSG
