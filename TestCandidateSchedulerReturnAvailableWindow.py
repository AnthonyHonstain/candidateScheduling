from datetime import datetime
import unittest

from CandidateScheduler import Block, _return_available_window


class TestCandidateSchedulerReturnAvailableWindow(unittest.TestCase):

  def test_return_available_window_no_next_block(self):
    '''
          start         end
           12pm  1230   1pm
            |------------|
      block |------|
      result       |-----|
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    previous_block = Block(datetime(2018, 7, 20, 12, 0), datetime(2018, 7, 20, 12, 30), 'X')
    next_block = None

    self.assertEqual(_return_available_window(previous_block, next_block, start, end),
                     (datetime(2018, 7, 20, 12, 30), end))

  def test_return_available_window_no_next_block_available_before(self):
    '''
           start        end
            12pm  1230  1pm
             |-----------|
      block        |-----|
      result No window
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    previous_block = Block(datetime(2018, 7, 20, 12, 30), datetime(2018, 7, 20, 13, 0), 'X')
    next_block = None

    self.assertEqual(_return_available_window(previous_block, next_block, start, end),
                     None)

  def test_return_available_window_single_overlapping_block(self):
    '''
          start         end
           12pm         1pm
            |------------|
      block |------------|
      result No window
    '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    previous_block = Block(datetime(2018, 7, 20, 12, 0), datetime(2018, 7, 20, 13, 0), 'X')
    next_block = None

    self.assertEqual(_return_available_window(previous_block, next_block, start, end),
                     None)

  def test_return_available_window_with_next_block(self):
    '''
         start         end
          12pm  1230   1pm
           |------------|
     block |------|     |------|
     result       |-----|
   '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    previous_block = Block(datetime(2018, 7, 20, 12, 0), datetime(2018, 7, 20, 12, 30), 'X')
    next_block = Block(datetime(2018, 7, 20, 13, 0), datetime(2018, 7, 20, 13, 30), 'X')

    self.assertEqual(_return_available_window(previous_block, next_block, start, end),
                     (datetime(2018, 7, 20, 12, 30), end))

  def test_return_available_window_no_blocks(self):
    '''
          start         end
           12pm  1230   1pm
            |------------|
     block none
     result |------------|
   '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 13, 0, 0)
    previous_block = None
    next_block = None

    self.assertEqual(_return_available_window(previous_block, next_block, start, end),
                     (start, end))

  def test_return_available_window_valid_window(self):
    '''
          start                             end
           12pm      1pm          2pm       3pm
            |--------------------------------|
     block  |----------|          |----------|
     result            |----------|
   '''
    start = datetime(2018, 7, 20, 12, 0, 0)
    end = datetime(2018, 7, 20, 15, 0, 0)
    previous_block = Block(datetime(2018, 7, 20, 12, 0), datetime(2018, 7, 20, 13, 0), 'X')
    next_block = Block(datetime(2018, 7, 20, 14, 0), datetime(2018, 7, 20, 15, 0), 'X')

    self.assertEqual(_return_available_window(previous_block, next_block, start, end),
                     (datetime(2018, 7, 20, 13, 0), datetime(2018, 7, 20, 14, 0)))


if __name__ == '__main__':
  unittest.main()
