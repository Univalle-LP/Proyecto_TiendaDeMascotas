from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Venta


@login_required
def ventas_api_list(request):
    ventas = Venta.objects.all().order_by('-creado_en')
    data = [
        {
            'id': venta.id,
            'total': float(venta.total),
            'estado': venta.estado,
            'fecha': venta.creado_en.isoformat() if venta.creado_en else None,
            'usuario': venta.usuario.nombre if venta.usuario else None,
        }
        for venta in ventas
    ]
    return JsonResponse({'ventas': data})

# Create your views here.
