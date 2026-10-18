#!/bin/bash
set -euo pipefail

repo_dir=/var/www/nolapatent-repo
web_dir=/var/www/nolapatent

if [[ $EUID -ne 0 ]]; then
    echo "Run this script as root or with sudo." >&2
    exit 1
fi

if [[ ! -d "$repo_dir/.git" ]]; then
    echo "Repository not found at $repo_dir. Clone it there first." >&2
    exit 1
fi

cd "$repo_dir"
git pull --ff-only

if [[ ! -f dist/index.html || ! -f dist/assets/site.css ]]; then
    echo "Generated website is missing. No files were copied or deleted." >&2
    exit 1
fi

rsync -rltp --delete --chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r "$repo_dir/dist/" "$web_dir/"

echo "NOLAPATENT updated successfully."
