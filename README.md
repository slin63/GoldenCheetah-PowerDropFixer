# GoldenCheetah-PowerDropFixer

Fixes power, cadence, and heart-rate gaps from signal drops that can't be fixed using GoldenCheetah's fix gaps in recording tool.

Mirrors the tolerance and stop settings in GC's fix gaps in recording tool.`Tolerance` defines minimum length of a signal drop to fix (inclusive). `Stop` defines maximum length of a signal drop to fix (exclusive).

Example usage:
-----

Let's say your power meter usually drops signal for 3 - 6 seconds. We can target these 3 - 6 second drops by setting `TOLERANCE=2` and `STOP=7` in the actual .py file (constants are listed in all caps at the top).
Cadence and HR values will be repaired as well, with the assumption that they dropped out at the same time power did.

The script assumes you're running it from your GC activities driectory. If you want to preview what the script will do to your activity file: `$python3 fixPower.py 2018_03_26_10_16_14.json --no-save`

If you want to save the proposed changes: `$python3 fixPower.py 2018_03_26_10_16_14.json --save`


Important Notes
-----
Will only work with GC formatted JSON activity files.
Intended for use with interval exercises only! Will produce exaggerated power values in races where coasting occurs often.

