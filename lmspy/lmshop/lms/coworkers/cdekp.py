from lms.coworkers.cdek import Cdek
from lms.defines import D6Y


class CdekP(Cdek):
    @property
    def key(self):
        return D6Y.CP
