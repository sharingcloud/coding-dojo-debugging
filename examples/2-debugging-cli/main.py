"""Main."""

from tasks.cli import TaskClient


def main():
    client = TaskClient()
    client.run()


if __name__ == "__main__":
    main()
