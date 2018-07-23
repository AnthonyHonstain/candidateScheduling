from collections import namedtuple

'''
A basic solution calculating available time periods for scheduling.

Testing
  The following command can run all the tests for the module:
    python -m unittest Test* -v
  Run a single test
    python TestCandidateSchedulerReturnAvailableWindow.py -v TestCandidateSchedulerReturnAvailableWindow.test_return_available_window_no_next_block
'''

# TODO - This extra object is primarily for debugging and in case I need know who is blocking
Block = namedtuple('Block', ['start', 'end', 'candidate'])


def calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration):
  '''
  Given the schedule blockers for two candidates, identify the segments between start and end times
  where both candidates are free and the time available is larger than the requested duration.

  :param candidate1_blockers: [(datetime, datetime),] list of tuples representing the (<start>, <end>) of schedule blockers
  :param candidate2_blockers: [(datetime, datetime),] list of tuples representing the (<start>, <end>) of schedule blockers
  :param start: The start window to consider scheduling.
  :param end: The end of the window to consider scheduling
  :param requested_duration: The amount of time requested.
  :return: [(datetime, datetime), ] List of tuples for (<start>,<end>) times that are available to schedule.
  '''
  combined_blocker_list = []

  for candidate_blocker in candidate1_blockers:
    combined_blocker_list.append(Block(candidate_blocker[0], candidate_blocker[1], 'C1'))
  for candidate_blocker in candidate2_blockers:
    combined_blocker_list.append(Block(candidate_blocker[0], candidate_blocker[1], 'C2'))

  combined_blocker_list.sort(key=lambda x: x.start)

  merged_blocker_list = _merge_blocker_list(combined_blocker_list)

  return _find_available_windows(merged_blocker_list, start, end, requested_duration)


def _find_available_windows(merged_blocker_list, start, end, requested_duration):
  available_windows = []
  previous_block = None

  for current_blocker in merged_blocker_list:
    if not previous_block:
      previous_block = current_blocker
      if start < previous_block.start:
        available_windows.append((start, previous_block.start))
    else:
      new_window = _validate_window(previous_block, current_blocker, start, end, requested_duration)
      if new_window:
        available_windows.append(new_window)

  new_window = _validate_window(previous_block, None, start, end, requested_duration)
  if new_window:
    available_windows.append(new_window)
  return available_windows


def _validate_window(previous_block, next_block, start, end, requested_duration):
  possible_window = _return_available_window(previous_block, next_block, start, end)
  if possible_window and possible_window[1] - possible_window[0] >= requested_duration:
    return possible_window
  return None


def _return_available_window(previous_block, next_block, start, end):
  '''
  This function can only consider windows that start AFTER the previous_block (NOT BEFORE)
  :param previous_block: Block(<start>, <end>, <candidate>)
  :param next_block: Block(<start>, <end>, <candidate>)
  :param start: datetime
  :param end: datetime
  '''
  # If no blocks, everything is available
  if not previous_block and not next_block:
    return start, end

  if not previous_block and next_block:
    raise Exception("Invalid case - cannot have next_block without previous_block")

  if start <= previous_block.end < end:
    # So if the previous block ends in the start/end range, we need to verify if next block
    # leaves us a space for a valid range (remember - they were already merged so there must
    # be a gap.
    if next_block:
      return previous_block.end, min(next_block.start, end)
    else:
      return previous_block.end, end

  return None


def _merge_blocker_list(combined_blocker_list):
  '''
  Combine schedule blockers that represent overlapping periods
  '''

  merged_blocker_list = []
  active_blocker = None

  for blocker in combined_blocker_list:
    if not active_blocker:
      active_blocker = blocker
    else:
      # discard - the next blocker is smaller than whats actively blockg
      if active_blocker.end >= blocker.end:
        continue
      # modify -
      if active_blocker.end >= blocker.start:
        # Need to merge these blocks
        active_blocker = Block(active_blocker.start, blocker.end, 'M')
      else:
        # These is a gap and these are not overlapping, start new blocker
        merged_blocker_list.append(active_blocker)
        active_blocker = blocker

  if active_blocker:
    merged_blocker_list.append(active_blocker)
  return merged_blocker_list
