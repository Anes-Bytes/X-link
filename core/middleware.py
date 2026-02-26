from core.services.domain_routing import extract_subdomain_from_host


class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.subdomain = extract_subdomain_from_host(request.get_host())

        if request.subdomain:
            request.urlconf = "config.subdomain_urls"

        return self.get_response(request)
