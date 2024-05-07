from rest_framework.response import Response


def aca(get_response):
    def middleware(request):
        response = get_response(request)
        if type(response) is Response:
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
        return response
    return middleware


def sid(get_response):
    def middleware(request):
        response = get_response(request)
        if type(response) is Response:
            try:
                response.data["sessionid"] = request.session.session_key
                response._is_rendered = False
                response.render()
            except (TypeError, ValueError, KeyError):
                pass
        return response
    return middleware
