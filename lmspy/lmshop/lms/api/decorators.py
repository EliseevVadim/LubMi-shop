from rest_framework.response import Response


def api_response(func):
    def tune_dict(result, flag: bool = True):
        if 'success' not in result:
            result['success'] = flag
        return result

    def deco(*args, **kwargs):
        result = func(*args, **kwargs)
        return Response(tune_dict(result)) if type(result) is dict \
            else Response({'success': False, 'why': result}) if type(result) is str \
            else Response({'success': result[0], 'why': result[1]}) if type(result) is tuple and len(result) == 2 and type(result[0]) is bool and type(result[1]) is str \
            else result
    return deco
