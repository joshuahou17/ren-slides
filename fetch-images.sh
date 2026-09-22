#!/usr/bin/env bash
# fetch-images.sh — pull the object photos the grid and problem/solution decks need.
# Run on your Mac, from the root of the ren-slides repo. Needs network; the Cowork
# container is blocked from every image host, which is why this isn't automated.
#
#   ./fetch-images.sh
#
# Each line is: <unsplash-photo-id-or-SEARCH> <target-filename> <what it's for>
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/photos

get () {  # get <id> <name>
  local id="$1" out="assets/photos/$2"
  [ -f "$out" ] && { echo "  have $2"; return; }
  curl -sSL -o "$out" "https://unsplash.com/photos/$id/download?force=true" \
    && echo "  got  $2" || echo "  FAIL $2"
}

echo "▸ picked already"
get b2jKJ4jAfkg wine-at-night.jpg          # blood-hrv-low + sleep-wake-at-3am: "Alcohol"

echo
echo "▸ still to choose — search Unsplash, pick a PORTRAIT shot, save under the name given:"
cat <<'LIST'
  "radiator bedroom"        -> warm-room.jpg        sleep-wake-at-3am : "A warm room"
  "empty dinner plate"      -> empty-plate.jpg      sleep-wake-at-3am : "Nothing since 5pm"
  "heavy meal late night"   -> late-dinner.jpg      sleep-deep-sleep-fix : "Late heavy dinner"
  "phone on kitchen counter"-> phone-away.jpg       sleep-deep-sleep-fix : "Phone in another room"
  "early dinner table"      -> early-dinner.jpg     sleep-deep-sleep-fix : "Eat 3 hours earlier"
  "alarm clock dark room"   -> alarm-clock.jpg      sleep-deep-sleep-fix : "Bedtime drifts 2 hours"
  "steamy shower bathroom"  -> hot-shower.jpg       sleep-deep-sleep-fix : "Hot shower at 11pm"
  "bathroom evening light"  -> early-shower.jpg     sleep-deep-sleep-fix : "Shower at 9:30"
LIST
echo
echo "Then: python3 src/render.py content/batch01/  — anything still missing an image"
echo "will name itself in the refusal."
