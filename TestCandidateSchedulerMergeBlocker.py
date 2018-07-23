from datetime import datetime
import unittest

from CandidateScheduler import Block, _merge_blocker_list


class TestCandidateSchedulerMergeBlocker(unittest.TestCase):

  def test_merge_blocker_list_empty(self):
    self.assertEqual(_merge_blocker_list([]), [])

  def test_merge_blocker_single_element(self):
    combined_blocker_list = [
      Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0), 'A'),
    ]
    result = _merge_blocker_list(combined_blocker_list)
    expected = [Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0), 'A')]
    self.assertEqual(result, expected)

  def test_merge_blocker_single_overlap(self):
    combined_blocker_list = [
      Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0), 'A'),
      Block(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0), 'B'),
    ]
    result = _merge_blocker_list(combined_blocker_list)
    expected = [Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 13, 0, 0), 'M')]
    self.assertEqual(result, expected)

  def test_merge_blocker_multiple_overlap(self):
    combined_blocker_list = [
      Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 12, 30, 0), 'A'),
      Block(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0), 'B'),
      Block(datetime(2018, 7, 20, 13, 00, 0), datetime(2018, 7, 20, 13, 30, 0), 'A'),
    ]
    result = _merge_blocker_list(combined_blocker_list)
    expected = [Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 13, 30, 0), 'M')]
    self.assertEqual(result, expected)

  def test_merge_blocker_with_blocker_larger_and_overlapping_several(self):
    '''
          12         13         14
       A   |---------------------|
       B         |----|
       B                    |----|
    '''
    combined_blocker_list = [
      Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 14, 0, 0), 'A'),
      Block(datetime(2018, 7, 20, 12, 30, 0), datetime(2018, 7, 20, 13, 0, 0), 'B'),
      Block(datetime(2018, 7, 20, 13, 30, 0), datetime(2018, 7, 20, 14, 0, 0), 'B'),
    ]
    result = _merge_blocker_list(combined_blocker_list)
    expected = [Block(datetime(2018, 7, 20, 12, 0, 0), datetime(2018, 7, 20, 14, 0, 0), 'A')]

    self.assertEqual(result, expected)


if __name__ == '__main__':
  unittest.main()
