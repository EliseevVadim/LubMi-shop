from lms.models import Parameter


def parameters_processor(_):  # TODO -- dont forget fixtures for params! --
    return {
        f'param_{p.key}': p.value for p in Parameter.objects.filter(in_context=True)
    }
