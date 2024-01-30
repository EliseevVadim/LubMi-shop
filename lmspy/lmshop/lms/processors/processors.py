from lms.models import Parameter


def parameters_processor(_):
    return {
        f'param_{p.key}': p.value for p in Parameter.objects.filter(in_context=True)
    }
