#!/bin/bash
# Count core agent lines (excluding channels/, cli/, providers/ adapters)
cd "$(dirname "$0")" || exit 1

echo "AEGIS core agent line count"
echo "================================"
echo ""

for dir in agent agent/tools bus config cron heartbeat session utils; do
  count=$(find "aegis/$dir" -maxdepth 1 -name "*.py" -exec cat {} + | wc -l)
  printf "  %-16s %5s lines\n" "$dir/" "$count"
done

root=$(cat aegis/__init__.py aegis/__main__.py | wc -l)
printf "  %-16s %5s lines\n" "(root)" "$root"

echo ""
total=$(find aegis -name "*.py" ! -path "*/channels/*" ! -path "*/cli/*" ! -path "*/providers/*" | xargs cat | wc -l)
echo "  Core total:     $total lines"
echo ""
echo "  (excludes: channels/, cli/, providers/)"
