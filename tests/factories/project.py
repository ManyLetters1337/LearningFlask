from projects.models import Project
from tests.factories.bases import ResourceFactory
from factory.fuzzy import FuzzyText


class ProjectFactory(ResourceFactory):
    class Meta:
        model = Project

    title = FuzzyText(length=20)
