import logging
from django.http import HttpResponseServerError
from django.template.response import TemplateResponse

logger = logging.getLogger(__name__)

class GlobalErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the error
        logger.exception(f"Unhandled exception: {str(exception)}")
        
        # Return a custom error response
        context = {
            'error_message': str(exception),
            'error_type': exception.__class__.__name__,
        }
        
        return TemplateResponse(request, 'error.html', context, status=500)