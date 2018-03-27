"""
Fixes power/cadence meter drop outs by filling in zero values with
the average of the last value before the signal dropped and the first
value that appears when the signal is reacquired.

Will produce inaccurate data for anything other than interval exercises.
"""

"""
BUGS:
why Doesn't this thing preserve ride tags/intervals?
    --> Fixed by using json_tricks to preserve ordering in the original .json file.
          - I have no idea why this matters
"""

import json_tricks
import codecs
import os
import argparse
from pprint import pprint

DIRECTORY_ACTIVITY = '/Users/sSDSD/Library/GoldenCheetah/shean/activities'
FILE_TEST = '/Users/sSDSD/Library/GoldenCheetah/shean/activities/2018_03_26_10_16_14.json'
TOLERANCE = 0 # <int> Minimum time gap to fill (exclusive)
STOP = 12     # <int> Maximum time gap to fill (inclusive)


def fix_zeroes(json_dir, save=False):
    with codecs.open(json_dir, 'r', 'utf-8-sig') as jsonfile:
        activity = json_tricks.load(jsonfile, preserve_order=True)

        timeseries = activity['RIDE']['SAMPLES']

        # Backup file as original.backup
        _backup_json(activity, json_dir)

        # Remove zeroes for power/cadence
        _fill_zeroes(timeseries)

        if save:
            # Overwrite original
            _output_json(activity, json_dir)

def _backup_json(data, output):
    with open(output + '.backup', 'w') as outfile:
        json_tricks.dump(data, outfile)
        console_log = "Backup saved to:\n{0}"
        print(console_log.format(output + '.backup'))

def _output_json(data, output):
    with open(output, 'w') as outfile:
        json_tricks.dump(data, outfile)
        console_log = "Saved to:\n{0}"
        print(console_log.format(output))


def _fill_zeroes(timeseries):
    """
    Counts number of consequentive zero power instances.
    When zero power instances exceed the tolerance but sit below the stop
    those values are overwritten with the average of the last and first signals received.
    """
    index = 0     # Current place we're moving through in the sample
    zero_power_index = 0 # First occurance of zero power
    zero_power_count = 0 # Consequetive instances of zero power

    power_last = 0       # Last power reading before signal lost
    power_first = 0      # First power reading when signal returns

    cad_last = 0         # Last cadence reading before signal lost
    cad_first = 0        # First cadence reading when signal returns

    samples_to_fill = 0  # Number of power samples to fill
    fill_value_pow = 0   # Power number to fill with
    fill_value_cad = 0   # Cadence number to fill with

    while index < len(timeseries):
        # print('INDEX=', index)

        power_current = timeseries[index]['WATTS']
        cadence_current = timeseries[index]['CAD']

        # Capture the last power/cad reading before power turns to zero
        if index > 0 and timeseries[index - 1]['WATTS'] != 0 and power_current == 0:

            power_last = timeseries[index - 1]['WATTS']
            cad_last = timeseries[index - 1]['CAD']

        # If not repairing data, track signal loss & develop fill values
        if samples_to_fill == 0:
            # Record the number of instances of zero power
            if power_current == 0:
                if zero_power_index == 0:    # If this is the first instance of zero power, record the occurance
                    zero_power_index = index

                zero_power_count += 1        # Increment zero power count


            # Either there is nothing wrong or the signal was regained
            elif power_current != 0:
                # Signal regained
                if TOLERANCE < zero_power_count <= STOP:
                    power_first = power_current
                    cad_first = cadence_current
                    samples_to_fill = zero_power_count

                    # Calculate fill values for power/cadence
                    fill_value_cad = __average_two_vals(cad_last, cad_first)
                    fill_value_pow = __average_two_vals(power_last, power_first)

                    console_log = "Fixing {0} samples with\n\tPOWER: {1}\n\tCAD: {2}\n\t"
                    print(console_log.format(samples_to_fill, fill_value_pow, fill_value_cad))

                    # Set current index to the first index that needs repairing
                    index = zero_power_index

                # Zero power count less than TOLERANCE or greater than STOP (signal was never lost or gap was too large)
                else:
                    zero_power_index = 0
                    zero_power_count = 0

                    power_last = 0
                    cad_last = 0



        # Otherwise, repair data with fill values
        else:
            timeseries[index]['WATTS'] = fill_value_pow
            timeseries[index]['CAD'] = fill_value_cad
            samples_to_fill -= 1

            # Once we've repaired all required samples, reset counter values and apply initial filling
            if samples_to_fill == 0:

                timeseries[zero_power_index]['WATTS'] = fill_value_pow
                timeseries[zero_power_index]['CAD'] = fill_value_cad

                zero_power_index = 0
                zero_power_count = 0

                power_last = 0
                power_first = 0

                cad_last = 0
                cad_first = 0

                samples_to_fill = 0
                fill_value_pow = 0
                fill_value_cad = 0

        index += 1


def __average_two_vals(a, b):
    print('AVG OF {0}, {1} = {2}'.format(a, b, ((a + b) / 2.0)))
    return (a + b) / 2.0


def __full_file_name(file_name):
    return os.getcwd() + '/' + file_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix power/cadence pair signal drops in GoldenCheetah .JSON activity files.')
    parser.add_argument('file', metavar='file', type=str, help='Name of JSON to be processed')
    parser.add_argument('--save', dest='save', action='store_true')
    parser.add_argument('--no-save', dest='save', action='store_false')
    parser.set_defaults(save=True)

    args = parser.parse_args()

    json_file = __full_file_name(args.file)

    print('RUNNING on {}'.format(json_file))
    fix_zeroes(json_file, args.save)
