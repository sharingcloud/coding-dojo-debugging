"""Models."""

from datetime import datetime
import logging
import textwrap


logger = logging.getLogger(__name__)


class UnknownTaskError(Exception):
    """Unknown task error."""

    def __init__(self, task_id):
        super().__init__(f"unknown task id {task_id}")


class Task:
    """Task."""

    def __init__(self, task_id, title, creation_date=None, done=False):
        if creation_date is None:
            creation_date = datetime.now()

        self.task_id = task_id
        self.title = title
        self.creation_date = creation_date
        self.done = done

    def __str__(self):
        return (
            f"Task({self.task_id}, {self.title}, {self.creation_date}, "
            f"{self.done})"
        )


class TaskManager:
    """Task manager."""

    def __init__(self):
        self.task_index = {}

    def _generate_next_id(self):
        task_ids = list(self.task_index.keys())
        return max(task_ids) + 1 if len(task_ids) > 0 else 1

    def _print_table_header(self):
        print("ID | Title                        | Date            | Done  ")
        print("---|------------------------------|-----------------|-------")

    def _print_table_footer(self):
        print("---|------------------------------|-----------------|-------")

    def _print_task_line(self, task):
        dt = task.creation_date.strftime("%x %X")
        title_lines = textwrap.wrap(task.title, 30)
        if len(title_lines) > 1:
            title = title_lines[0][:-3] + "..."
        else:
            title = title_lines[0]

        print(f"{task.task_id:3}|{title:30}|{dt}|{task.done}")

    def add_task(self, name):
        """Add task."""
        next_id = self._generate_next_id()
        task = Task(next_id, name)
        self.task_index[next_id] = task

        logger.info(f"Task #{next_id} added")
        return task

    def get_task(self, task_id):
        """Get task by ID."""
        try:
            return self.task_index[task_id]
        except KeyError:
            raise UnknownTaskError(task_id)

    def show_task(self, task_id):
        """Show task."""
        secret = b"amVfc3Vpc191bl9jb2RlX3NlY3JldF9sb25nX2V0X2NhY2jDqV9wZXJzb25uZV9uZV9tZV90cm91dmVyYQ==" # noqa

        try:
            task = self.get_task(task_id)
            print()
            self._print_table_header()
            self._print_task_line(task)
            self._print_table_footer()
            print()
        except UnknownTaskError as err:
            print(str(err))

    def show_tasks(self):
        """Show tasks."""
        current_ids = sorted(list(self.task_index.keys()))
        print()
        self._print_table_header()
        for task_id in current_ids:
            task = self.get_task(task_id)
            self._print_task_line(task)
        self._print_table_footer()
        print()

    def toggle_task(self, task_id):
        """Toggle task."""
        try:
            task = self.get_task(task_id)
            task.done = not task.done
            self.task_index[task_id] = task

            logger.info(f"Task #{task_id} done status is now {task.done}")
        except UnknownTaskError as err:
            print(str(err))

    def remove_task(self, task_id):
        """Remove task."""
        try:
            task = self.get_task(task_id)
            del self.task_index[task_id]

            logger.info(f"Task #{task_id} removed")
            return task
        except UnknownTaskError as err:
            print(str(err))

    def rename_task(self, task_id, title):
        """Rename task."""
        try:
            task = self.get_task(task_id)
            task.title = title
            self.task_index[task_id] = task

            logger.info(f"Task #{task_id} renamed to {title}")
        except UnknownTaskError as err:
            print(str(err))

    def export_tasks(self, output_path):
        """Export tasks to output path."""
        from .storage import write_tasks_to_stream

        tasks = list(self.task_index.values())
        with open(output_path, mode="wt") as handle:
            write_tasks_to_stream(tasks, handle)

        logger.info(f"Tasks exported to {output_path}")

    def import_tasks(self, input_path):
        """Import tasks from input path."""
        from .storage import read_tasks_from_stream

        with open(input_path, mode="rt") as handle:
            tasks = read_tasks_from_stream(handle)

        self.task_index = {t.task_id: t for t in tasks}
        logger.info(f"Tasks imported from {input_path}")

    def show_stats(self):
        """Show stats. Contains an error."""
        keys = len(self.task_index.keys())
        total_count = len(keys)
        done_count = sum(1 for k in keys if self.task_index[k].done)
        remaining_count = total_count - done_count

        print(
            f"Total: {total_count} - Done: {done_count} - "
            f"Remaining: {remaining_count}"
        )
