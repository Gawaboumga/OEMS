from pymatex import search
from api import models


class LatexFinder:
    class __LatexFinder:
        def __init__(self):
            pass

        def __str__(self):
            return repr(self)

    instance = None
    search_query = None

    def __init__(self):
        if not LatexFinder.instance:
            LatexFinder.instance = LatexFinder.__LatexFinder()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def add(self, pk: int, latex: str):
        LatexFinder.search_query.add(pk, latex)

    def is_valid(self, latex: str):
        LatexFinder.search_query.is_valid(latex)

    def load(self, path: str):
        LatexFinder.search_query = search.SearchQuery(path=path)

    def remove(self, pk: int):
        LatexFinder.search_query.remove(pk)

    def save(self, path: str):
        with open(path, 'w') as f:
            for mathematical_object in models.MathematicalObject.objects.all():
                f.write('{}: {}\n'.format(mathematical_object.pk, mathematical_object.latex))

    def search(self, latex: str):
        return LatexFinder.search_query.search(latex)
