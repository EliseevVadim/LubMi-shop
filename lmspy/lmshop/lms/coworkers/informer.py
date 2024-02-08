from lms.models import Region, City


class Informer:
    instance = None

    def __new__(cls):
        def create():
            Informer.instance = super(Informer, cls).__new__(cls)
            return Informer.instance
        return Informer.instance if Informer.instance else create()

    def __init__(self):
        self.index: dict[str, set[int]] = dict()

        for city in City.objects.all():
            print(city)