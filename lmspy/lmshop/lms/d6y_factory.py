from lms.coworkers.cdek import Cdek
from lms.coworkers.cdekp import CdekP
from lms.coworkers.postru import PostRu
from lms.d6y import D6Y


def ds_factory(selector):
    builders = {
        D6Y.CD: lambda: Cdek(),
        D6Y.CP: lambda: CdekP(),
        D6Y.PR: lambda: PostRu()
    }
    return builders[selector]()
