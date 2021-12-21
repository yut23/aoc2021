#!/bin/bash
set -euo pipefail
day=${1:-$(date +%-e)}
session=$(<.aoc_session)
curl "https://adventofcode.com/2021/day/$day/input" --cookie "session=$session" -o "input/day$day.txt"
