# GoldenCheetah-PowerDropFixer

Fixes power gaps from signal drops that can't be fixed using GoldenCheetah's fix gaps in recording tool.

Mirrors the tolerance and stop settings in GC's fix gaps in recording tool.`Tolerance` defines minimum length of a signal drop to fix (inclusive). `Stop` defines maximum length of a signal drop to fix (exclusive).

##### Important Notes
Will only work with GC formatted JSON activity files.
Intended for use with interval exercises only! Will produce exaggerated power values in races where coasting occurs often.

### Example usage:

If you want to preview what the script will do to your activity file.
`$python3 fixPower.py 2018_03_26_10_16_14.json --no-save`

If you want to save the proposed changes.
`$python3 fixPower.py 2018_03_26_10_16_14.json --save`

