def ACAO(get_response):
    def middleware(request):
        response = get_response(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return middleware
