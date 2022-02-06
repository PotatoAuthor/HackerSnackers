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
    # Find the length and time of free blocks of time
    run_length = run_lengths(occupied)
    # Find the start time to look at indices of run_length in context of
    start_time = (datetime.datetime.now() + datetime.timedelta(
        minutes=15 - (datetime.datetime.now().minute % 15))).replace(microsecond=0, second=0)
    free_times_hi = []
    for i in run_length:
        # The start of the specific free time block
        start_time_free = start_time + datetime.timedelta(minutes=15 * i)
        # The end of the specific free time block
        end_time_free = start_time_free + datetime.timedelta(minutes=15 * run_length[i])
        # Bounds to restrict free time blocks in the day
        morning_bound_start = start_time_free.replace(hour=8, minute=0)
        night_bound_start = start_time_free.replace(hour=22, minute=0)
        morning_bound_end = end_time_free.replace(hour=8, minute=0)
        night_bound_end = end_time_free.replace(hour=22, minute=0)
        # If free time blocks are partially in nighttime hours, then we truncate them
        # Otherwise, that free time is not added
        if (morning_bound_start <= start_time_free <= night_bound_start and
                morning_bound_end <= end_time_free <= night_bound_end):
            pass
        elif (morning_bound_start <= start_time_free <= night_bound_start and
              (end_time_free > night_bound_end or end_time_free < morning_bound_end)):
            end_time_free = end_time_free.replace(hour=22, minute=0)
        elif ((start_time_free > night_bound_start or start_time_free < morning_bound_start)
              and morning_bound_end <= end_time_free <= night_bound_end):
            start_time_free = start_time_free.replace(hour=8, minute=0)
        else:
            continue
        # Adding the starting time, ending time and number of 15 minute blocks of free time
        free_times_hi.append((start_time_free, end_time_free, run_length[i]))
    return free_times_hi


def run_lengths(occupied: list[int]) -> dict[int, int]:
    """
    Track the length and starting index of the runs of number 1
    :param occupied: A list of 0's and 1's that reflect whether the i'th fifteen minute interval has
    any events for intervals extending from now.
    """
    run_length = {}
    start = 0
    # We find the first free block
    while occupied[start] != 0:
        start += 1
    for i in range(start, len(occupied)):
        # We don't add to our runs until we reach a one and our current run stops
        if occupied[i] == 1:
            run_length[start] = i - start
            # In the case the next number is also a one, that index gets a value of zero
            # in dictionary
            start = i + 1
    # We make sure we capture the last run of 0's if we don't encounter a one until end of array
    if occupied[len(occupied) - 1] == 0:
        run_length[start] = len(occupied) - start
    # Then we take out all key-value pairs which had a value, or run-length of 0, as that meant
    # That index had a 1
    run_length = {key: run_length[key] for key in run_length if run_length[key] != 0}
    return run_length

# Testing
# if __name__ == '__main__':
#     hi = [1, 1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0]
#     print(run_lengths(hi))
#     print(free_times(hi))
#     print((datetime.datetime.now() + datetime.timedelta(
#         minutes=15 - (datetime.datetime.now().minute % 15))).replace(microsecond=0, second=0) + datetime.timedelta(
#         minutes=15 * 20))
