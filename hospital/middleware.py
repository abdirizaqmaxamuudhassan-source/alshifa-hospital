from .i18n_so import translate_html
class LanguageMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if (request.session.get("lang") == "so" and not request.path.startswith("/admin")
                and not response.streaming and response.get("Content-Type", "").startswith("text/html")):
            response.content = translate_html(response.content.decode("utf-8")).encode("utf-8")
            if response.has_header("Content-Length"): response["Content-Length"] = str(len(response.content))
        return response
