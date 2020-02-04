from notes.models import Note
from tests.factories.bases import ResourceFactory
from factory.fuzzy import FuzzyText


class NoteFactory(ResourceFactory):
    class Meta:
        model = Note

    title = FuzzyText(length=20)
    status = "Active"

