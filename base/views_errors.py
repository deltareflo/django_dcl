from django.shortcuts import render

def error_404(request, exception):
    """
    Vista personalizada para manejar errores 404 (Página no encontrada)
    """
    return render(request, 'base/404.html', status=404)

def error_500(request):
    """
    Vista personalizada para manejar errores 500 (Error del servidor)
    """
    return render(request, 'base/500.html', status=500)