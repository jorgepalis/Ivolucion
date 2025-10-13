from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Llama al manejador por defecto de DRF primero
    response = exception_handler(exc, context)

    if response is not None:
        # Si la respuesta contiene 'detail', muévelo a 'error'
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                response.data = {'error': response.data['detail']}
            else:
                # Para validaciones, errores de campos, etc.
                response.data = {'error': response.data}
    else:
        # Si no hay respuesta, es un error inesperado
        response = {
            'error': 'Error interno del servidor. Por favor intente más tarde.'
        }

    return response
