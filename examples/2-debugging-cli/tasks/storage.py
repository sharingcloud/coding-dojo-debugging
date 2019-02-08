"""Storage utils."""

from datetime import datetime
import json


def serialize_task(task):
    return {
        "task_id": task.task_id,
        "title": task.title,
        "creation_date": task.creation_date.strftime("%x %X"),
        "done": task.done
    }


def deserialize_task(data):
    from .models import Task
    return Task(
        data["task_id"],
        data["title"],
        datetime.strptime(data["creation_date"], "%x %X"),
        data["done"]
    )


def deserialize_tasks(data):
    return [deserialize_task(t) for t in data]


def serialize_tasks(tasks):
    return [serialize_task(t) for t in tasks]


def write_tasks_to_stream(tasks, stream):
    json_serialized = json.dumps(serialize_tasks(tasks))
    stream.write(json_serialized)


def read_tasks_from_stream(stream):
    json_serialized = json.loads(stream.read())
    return deserialize_tasks(json_serialized)
