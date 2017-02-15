from TaskQueue import TaskQueue
import unittest

class MainTestCase(unittest.TestCase):
    def setUp(self):
        # create tasks
        self.queue = TaskQueue()
        self.queue.clear_table(table_name='tasks')
        self.queue.clear_table(table_name='queue')

    def tearDown(self):
        self.queue.clear_table(table_name='tasks')
        self.queue.clear_table(table_name='queue')

    def test_complete_task(self):
        print 'Testing complete_task() method'
        task_id = self.queue.create_task(urgency = 'week')
        print 'Created a task with id={}'.format(task_id)

        # task hasn't been assigned yet so it's not pending and should raise error
        with self.assertRaises(ValueError):
            self.queue.complete_task(task_id)
            print 'Task is not pending'

        test_scaler_id = 1
        newly_assigned_task = self.queue.receive_tasks(test_scaler_id, 1)[0]

        self.queue.complete_task(newly_assigned_task)
        print 'Completed task {}'.format(newly_assigned_task)

        self.assertEqual(len(self.queue), 0, 'Completed task was not removed from the queue.')

    def test_receive_tasks(self):
        print '\nTesting receive_tasks() method'
        task_id1 = self.queue.create_task(urgency = 'immediate')
        task_id2 = self.queue.create_task(urgency = 'immediate')
        task_id3 = self.queue.create_task(urgency = 'immediate')
        print 'Created 3 tasks'

        test_scaler_id = 2
        newly_assigned_tasks = self.queue.receive_tasks(test_scaler_id, 2)
        print 'Assigned tasks {} to scaler {}'.format(str(newly_assigned_tasks), test_scaler_id)

        for task_id in newly_assigned_tasks:
            is_status_pending = self.queue.check_status(task_id=task_id, status='PENDING')
            self.assertTrue(is_status_pending, 'Task was not properly assigned')

if __name__ == '__main__':
    unittest.main()

