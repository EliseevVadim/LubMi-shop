from lms.coworkers.cdek import Cdek


class Informer:
    def __init__(self):
        self._cities: dict[int, dict] = dict()
        self._search: dict[str, int] = dict()

    def load_cdek(self):
        print("-----------------------------------------")
        cdek = Cdek()
        page = 0
        size = 1000
        while True:
            pack = cdek.regions(size=size, page=page)

            if len(pack):
                for r in pack:
                    print(r)
                page += 1
            else:
                break


