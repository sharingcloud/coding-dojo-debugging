"""CLI."""

from collections import OrderedDict
import logging
import logging.config

import questionary

from .config import LOGGING
from .models import TaskManager


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """
Welcome to the task manager!
"""

ACTION_HANDLERS = OrderedDict({
    'show task list': '_show_task_list',
    'show task': '_show_task',
    'add task': '_add_task',
    'toggle task': '_toggle_task',
    'rename task': '_rename_task',
    'remove task': '_remove_task',
    'export tasks': '_export_tasks',
    'import tasks': '_import_tasks',
    'stats (buggy)': '_show_stats',
    'exit': '_exit'
})


class TaskClient:
    def __init__(self):
        self.mgr = TaskManager()

    def run(self):
        logger.info("Running task client...")
        print(WELCOME_MESSAGE)

        self.mgr.show_tasks()

        running = True
        while running:
            try:
                running = self.prompt_action()
            except KeyboardInterrupt:
                pass
            except Exception as exc:
                logger.exception(exc)

        logger.info("Stopping task client...")

    def prompt_action(self):
        choice = questionary.select(
            "What do you want to do?",
            choices=list(ACTION_HANDLERS.keys())
        ).ask()

        return getattr(self, ACTION_HANDLERS[choice])()

    def _show_task_list(self):
        self.mgr.show_tasks()
        return True

    def _show_task(self):
        task_id = int(questionary.text("Task ID").ask())
        self.mgr.show_task(task_id)
        return True

    def _add_task(self):
        title = questionary.text("Title").ask()
        task = self.mgr.add_task(title)
        self.mgr.show_task(task.task_id)
        return True

    def _toggle_task(self):
        task_id = int(questionary.text("Task ID").ask())
        self.mgr.toggle_task(task_id)
        self.mgr.show_task(task_id)
        return True

    def _rename_task(self):
        task_id = int(questionary.text("Task ID").ask())
        title = questionary.text("Title").ask()
        self.mgr.rename_task(task_id, title)
        self.mgr.show_task(task_id)
        return True

    def _remove_task(self):
        task_id = int(questionary.text("Task ID").ask())
        self.mgr.remove_task(task_id)
        self.mgr.show_tasks()
        return True

    def _export_tasks(self):
        path = questionary.text("Output path").ask()
        self.mgr.export_tasks(path)
        return True

    def _import_tasks(self):
        path = questionary.text("Input path").ask()
        self.mgr.import_tasks(path)
        self.mgr.show_tasks()
        return True

    def _show_stats(self):
        self.mgr.show_stats()
        return True

    def _exit(self):
        return False
