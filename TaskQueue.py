import os

from datetime import datetime, timedelta
from sqlobject import sqlhub, connectionForURI
from sqlobject.sqlbuilder import Delete
from sqlobject.sqlbuilder import Insert
from sqlobject.sqlbuilder import Select
from sqlobject.sqlbuilder import sqlrepr
from sqlobject.sqlbuilder import Table
from sqlobject.sqlbuilder import Update

class TaskQueue(object):
    """Task Queue class that handles assigning and
    un-assigning tasks to different Scalers."""

    def __init__(self):
        self.db_url = os.environ['DATABASE_URL']
        self.connection = connectionForURI(self.db_url)
        sqlhub.processConnection = self.connection

    def __len__(self):
        count_queue_tasks = "SELECT COUNT(task_id) FROM queue"
        row = self.connection.queryAll(count_queue_tasks)
        length = row[0][0]

        return length

    def create_task(self, urgency):
        """Creates a task with the given urgency.

        Args:
            urgency: one of immediate, day, or week.

        Returns:
            The created task object

        """
        if urgency.lower() == 'immediate':
            additional = timedelta(hours=1)
        elif urgency.lower() == 'day':
            additional = timedelta(days=1)
        elif urgency.lower() == 'week':
            additional = timedelta(weeks=1)
        else:
            additional = None
            raise ValueError("Urgency must be 'immediate', 'day', or 'week'")

        created_at = str(datetime.now())
        complete_by = str(datetime.now() + additional)
        completed_at = None
        status = 'READY'
        assigned_to = ''

        task_table = Table('tasks')

        insert_task = Insert(task_table, values={
            'created_at': created_at,
            'complete_by': complete_by,
            'completed_at': completed_at,
            'status': status,
            'urgency': urgency
        })

        task_query = self.connection.sqlrepr(insert_task)
        self.connection.query(task_query)

        get_id_query = "SELECT currval('tasks_id_seq')"
        row = self.connection.queryAll(get_id_query)
        task_id = int(row[0][0])

        self._enqueue(task_id=task_id, complete_by=complete_by)

        return task_id


    def complete_task(self, task_id):
        """Marks the given pending task as completed

        Returns:
            The updated task id

        """

        if not self.check_status(task_id, 'PENDING'):
            raise ValueError("Task with id={} was not pending".format(task_id))

        self._change_status(task_id=task_id, new_status='COMPLETED')
        self._dequeue(task_id=task_id)

        return task_id

    def cancel_task(self, task_id):
        """Marks the given pending task as canceled, only if it's not completed.

        Returns:
            The updated task id

        """
        if not self.check_status(task_id, 'PENDING'):
            raise ValueError("Task with id={} was not pending".format(task_id))

        self._change_status(task_id=task_id, new_status='CANCELED')
        self._dequeue(task_id=task_id)

        return task_id

    def receive_tasks(self, scaler_id, batch_size):
        """Assigns a batch of the highest priority batch_size tasks to
        Scaler with scaler_id.

        Returns:
            The batch of assigned task ids in a list

        """
        task_table = Table('tasks')

        select_tasks = Select(
            items=['task_id'],
            staticTables=['queue'],
            limit=batch_size,
            orderBy='complete_by'
        )

        query = self.connection.sqlrepr(select_tasks)
        batch = self.connection.queryAll(query)

        task_ids = [int(t[0]) for t in batch]

        for _id in task_ids:
            self._change_status(task_id=_id, new_status='PENDING')

            update_task = Update(task_table,
                values={'assigned_to': scaler_id},
                where='id={}'.format(_id))

            update_query = self.connection.sqlrepr(update_task)
            self.connection.query(update_query)

        return task_ids

    def unassign_tasks(self, scaler_id):
        """Unassigns all tasks assigned to the Scaler with given scaler_id

        Returns:
            The unassigned task ids in a list

        """
        task_table = Table('tasks')
        get_tasks = Select(
            items=['id'],
            staticTables=['tasks'],
            where='assigned_to={}'.format(scaler_id)
        )

        query = self.connection.sqlrepr(get_tasks)
        assigned_tasks = self.connection.queryAll(query)

        task_ids = [int(t[0]) for t in batch]
        clauses = [task_table.id == iden for iden in task_ids]
        where_statement = OR(*clauses)

        update_statuses = Update(task_table,
                values={'status': 'READY'},
                where=where_statement)

        update_assignments = Update(task_table,
                values={'assigned_to': None},
                where=where_statement)

        update_query1 = self.connection.sqlrepr(update_statuses)
        update_query2 = self.connection.sqlrepr(update_assignments)
        self.connection.query(update_query1)
        self.connection.query(update_query2)

        return task_ids

    def check_status(self, task_id, status):
        get_status_query = "SELECT status FROM tasks WHERE id={}".format(task_id)
        row = self.connection.queryAll(get_status_query)
        task_status = row[0][0]

        return task_status.lower() == status.lower()

    def clear_table(self, table_name):
        clear_table_query = "DELETE FROM {}".format(table_name)
        self.connection.query(clear_table_query)

        return

    def _enqueue(self, task_id, complete_by):
        queue_table = Table('queue')

        push_queue = Insert(queue_table, values={
            'task_id': task_id,
            'complete_by': complete_by
        })

        queue_query = self.connection.sqlrepr(push_queue)
        self.connection.query(queue_query)

        return

    def _dequeue(self, task_id):
        queue_table = Table('queue')

        where_statement = 'task_id={}'.format(task_id)
        pop_queue = Delete(queue_table, where=where_statement)

        queue_query = self.connection.sqlrepr(pop_queue)
        self.connection.query(queue_query)

        return

    def _change_status(self, task_id, new_status):
        task_table = Table('tasks')

        where_statement = 'id={}'.format(task_id)
        update_task = Update(task_table, values={'status': new_status},
            where=where_statement)

        task_query = self.connection.sqlrepr(update_task)
        self.connection.query(task_query)

        if new_status == 'COMPLETED':
            update = Update(task_table, values={'completed_at': str(datetime.now())},
                where=where_statement)

            task_query = self.connection.sqlrepr(update)
            self.connection.query(task_query)

        return
