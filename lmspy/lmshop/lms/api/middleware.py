from rest_framework.response import Response


def axios_crutches(get_response):
    def middleware(request):
        response = get_response(request)
        if type(response) is Response:
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
        return response
    return middleware
