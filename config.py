"""
App Config
"""
from enum import Enum

page_size = 5


class Statuses(Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
