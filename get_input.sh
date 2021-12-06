#!/bin/bash
set -euo pipefail
day=${1:-$(date +%-e)}
curl "https://adventofcode.com/2021/day/$day/input" --cookie "session=$(<.aoc_session)" > "input/day$day.txt"
