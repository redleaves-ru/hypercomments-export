import os
import sys


def get_current_path(local_path):
    return os.path.join(os.path.dirname(__file__), local_path)


if __name__ == '__main__':
    sys.path.append(get_current_path('example'))
    from exporter import export
    export(get_current_path('example/input/HyperCommentsFull.html'), get_current_path('example/output.json'))
