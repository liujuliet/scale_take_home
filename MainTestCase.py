from TaskQueue import TaskQueue
import unittest

class MainTestCase(unittest.TestCase):
    def setUp(self):
        # create tasks
        self.queue = TaskQueue()

    def tearDown(self):
        pass

    def test_create_task(self):
        urgency = 'week'
        task_id = self.queue.create_task(urgency)

        print task_id

if __name__ == '__main__':
    unittest.main()

