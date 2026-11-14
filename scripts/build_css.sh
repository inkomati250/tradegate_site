#!/usr/bin/env bash
# Rebuilds website/static/website/css/site.css from the templates.
# Run after changing classes in templates, then commit the CSS file.
set -euo pipefail
cd "$(dirname "$0")/.."
npx --yes tailwindcss@3.4.19 -c tailwind/tailwind.config.js -i tailwind/input.css -o website/static/website/css/site.css --minify
