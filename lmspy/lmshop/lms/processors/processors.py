from lms.models import Parameter


def parameters_processor(request):
    return {
        f'param_{p.key}': p.value for p in Parameter.objects.all() if p.in_context
    }
