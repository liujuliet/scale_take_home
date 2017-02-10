import pymongo
import scaleapi

client = scaleapi.ScaleClient('test_9e67acbe57b6d485599b9511ce240976')

# * task_id
#     * unique identifier of the task
# * created_at
#     * timestamp of creation
# * completed_at
#     * timestamp of completion
# * status
#     * One of pending, canceled, or completed.
# * urgency
#     * one of immediate, day, or week.
#         *  immediate means it's to be completed within 1 hour
#         *  day is to be completed within 1 day
#         *  week is to be completed within 1 week.

class TaskQueue(object):
    """Task Queue class that handles assigning and
    un-assigning tasks to different Scalers."""

    def __init__(self):
        self.queue = []

    def create_task(self, urgency):
        """Creates a task with the given urgency.

        Args:
            urgency: one of immediate, day, or week.

        Returns:
            The created task object

        """

    def complete_task(self, task_id):
        """Marks the given pending task as completed >> API CALL

        Returns:
            The updated task object

        """

    def cancel_task(self, task_id):
        """Marks the given pending task as canceled, only if it's not completed.

        The endpoint (me) will return a 500 error code if you attempt to
        cancel a completed task.

        Returns:
            The updated task object

        """

    def receive_tasks(self, scaler_id, batch_size):
        """Assigns a batch of the highest priority batch_size tasks to
        Scaler with scaler_id

        Returns:
            The batch of assigned tasks in a list

        """

    def unassign_tasks(self, scaler_id):
        """Unassigns all tasks assigned to the Scaler with given scaler_id

        Returns:
            The unassigned tasks in a list

        """

