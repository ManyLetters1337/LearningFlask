"""
App Config
"""
from enum import Enum
import os

page_size = 5

secret_key = os.urandom(24)


class Statuses(Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
