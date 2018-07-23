from datetime import datetime, timedelta
import unittest

from CandidateScheduler import calculate_open_schedules


class TestCandidateScheduler(unittest.TestCase):

  def test_no_blockers_with_valid_start_and_end(self):
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=10)

    self.assertEqual(calculate_open_schedules([], [], start, end, requested_duration),
                     [(start, end), ])

  def test_duration_larger_than_possible(self):
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=61)

    self.assertEqual(calculate_open_schedules([], [], start, end, requested_duration),
                     [])

  def test_blockers_with_no_available(self):
    '''
          start         end
           12pm  1230   1pm
            |------------|
     block  |------------|
     result No window
   '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=10)

    candidate1_blockers = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 13, 0, 0))]
    candidate2_blockers = []

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    self.assertEqual(result, [])

  def test_candidate1_has_blocker_and_candidate2_free(self):
    '''
             start         end
              12pm  1230   1pm
               |------------|
     C1 block  |------|
     C2 block
     result           |-----|
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=10)

    candidate1_blockers = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0))]
    candidate2_blockers = []

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    expected_result = [(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0))]
    self.assertEqual(result, expected_result)

  def test_candidate1_has_blocker_but_requested_time_to_large(self):
    '''
             start         end
              12pm  1230   1pm
               |------------|
     C1 block  |------|
     C2 block
     result  No window because of requested duration
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=31)

    candidate1_blockers = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0))]
    candidate2_blockers = []

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    expected_result = []
    self.assertEqual(result, expected_result)

  def test_single_blocker(self):
    '''
             start                end
              12pm  1230   2pm   230pm
               |--------------------|
     C1 block         |------|
     C2 block
     result    |------|      |------|
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 30, 0)
    requested_duration = timedelta(minutes=30)

    candidate1_blockers = []
    candidate2_blockers = [(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0))]

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    expected_result = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0)),
                       (datetime(2018, 7, 20, 13, 0, 0), datetime(2018, 7, 20, 13, 30, 0))]
    self.assertEqual(result, expected_result)

  def test_overlapping_blockers(self):
    '''
               start         end
                12pm  1230   2pm
                 |-------------|
     C1 block    |------|
     C2 block    |------|
     result             |------|
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=10)

    candidate1_blockers = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0))]
    candidate2_blockers = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0))]

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    expected_result = [(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0))]
    self.assertEqual(result, expected_result)

  def test_blocking_window_larger_than_start(self):
    '''
               start         end
                12pm  1230   2pm
                 |------------|
     C1 block |--------|
     C2 block
     result            |------|
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=10)

    candidate1_blockers = [(datetime(2018, 7, 20, 11, 0, 0), datetime(2018, 7, 20, 12, 30, 0))]
    candidate2_blockers = []

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    expected_result = [(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0))]
    self.assertEqual(result, expected_result)

  def test_blocking_window_larger_than_end(self):
    '''
             start          end
              12pm  1230    1pm
               |-------------|
     C1 block         |------|
     C2 block
     result    |------|
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    requested_duration = timedelta(minutes=10)

    candidate1_blockers = [(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 30, 0))]
    candidate2_blockers = []

    result = calculate_open_schedules(candidate1_blockers, candidate2_blockers, start, end, requested_duration)
    expected_result = [(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0))]
    self.assertEqual(result, expected_result)


if __name__ == '__main__':
  unittest.main()

