"""Creates function that will give free times in one's schedule"""

import datetime
from typing import List, Tuple


def free_times(occupied: list[int]) -> \
        List[Tuple[datetime.datetime, datetime.datetime, int]]:
    """
    Returns a list of tuples containing the start and finish times of free blocks of time
    that are between 8 am and 10 pm, and truncates if necessary, and the
    number of 15 minute intervals that pass between them

    :param occupied: A list of 0's and 1's that reflect whether the i'th fifteen minute interval has
    any events for intervals extending from now.
    """
    run_length = run_lengths(occupied)
    start_time = (datetime.datetime.now() + datetime.timedelta(
        minutes=15 - (datetime.datetime.now().minute % 15))).replace(microsecond=0, second=0)
    free_times = []
    for i in run_length:
        start_time_free = start_time + datetime.timedelta(minutes=15 * i)
        end_time_free = start_time_free + datetime.timedelta(minutes=15 * run_length[i])
        morning_bound_start = start_time_free.replace(hour=8, minute=0)
        night_bound_start = start_time_free.replace(hour=22, minute=0)
        morning_bound_end = end_time_free.replace(hour=8, minute=0)
        night_bound_end = end_time_free.replace(hour=22, minute=0)
        if (morning_bound_start <= start_time_free <= morning_bound_end and
                night_bound_start <= end_time_free <= night_bound_end and
                end_time_free.day == start_time_free.day):
            pass
        elif (morning_bound_start <= start_time_free <= morning_bound_end and
              (end_time_free > night_bound_end or end_time_free < night_bound_start)
              and end_time_free.day == start_time_free.day):
            end_time_free = end_time_free.replace(hour=22)
        elif ((start_time_free > morning_bound_end or start_time_free < morning_bound_start)
              and night_bound_start <= end_time_free <= night_bound_end and
              end_time_free.day == start_time_free.day):
            start_time_free = start_time_free.replace(hour=8)
        else:
            continue
        free_times.append((start_time_free, end_time_free, run_length[i], i))
    return free_times


def run_lengths(occupied: list[int]) -> dict[int, int]:
    """
    Track the length and starting index of the runs of number 1
    :param occupied: A list of 0's and 1's that reflect whether the i'th fifteen minute interval has
    any events for intervals extending from now.
    """
    run_length = {}
    start = 0
    while occupied[start] != 0:
        start += 1
    for i in range(start, len(occupied)):
        if occupied[i] == 1:
            run_length[start] = i - start
            start = i + 1
    if occupied[len(occupied) - 1] == 0:
        run_length[start] = len(occupied) - start
    run_length = {key: run_length[key] for key in run_length if run_length[key] != 0}
    return run_length

# Testing
if __name__ == '__main__':
    hi = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
          1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
          1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
          0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print(run_lengths(hi))
    print(free_times(hi))
    print((datetime.datetime.now() + datetime.timedelta(
        minutes=15 - (datetime.datetime.now().minute % 15))).replace(microsecond=0, second=0) + datetime.timedelta(
        minutes=15 * 20))
