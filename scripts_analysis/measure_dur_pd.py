# Measures duration and continuity of the dataset in pandas format. To be used as a part in other code.
# Author: Patrik Goldschmidt (igoldschmidt@fit.vut.cz)

import pd

# Are there gaps in the data (was the capture interrupted?)
def measure_real_capture_dur(data: pd.Series, gap_max_secs: int = 600) -> float:
    """Computes total timespan of the capture. Expects iterable containing timestamps objects sorted in a descending manner"""
    total_dur = 0
    current_dur = 0
    cont_durations = []
    last_tstamp = data.iloc[0]
    contiguous = True

    # Iterate through the dataframe to find out gaps
    for cur_tstamp in data:
        dur_gap = last_tstamp - cur_tstamp

        if dur_gap <= gap_max_secs:
            total_dur += dur_gap
            current_dur += dur_gap
        else:
            cont_durations.append(current_dur)
            current_dur = 0

            if contiguous:
                contiguous = False

        last_tstamp = cur_tstamp

    cont_durations.sort(key=int, reverse=True)
    cont_durations = [pd.Timedelta(seconds=secs) for secs in cont_durations]

    return pd.Timedelta(seconds=total_dur), contiguous, cont_durations

