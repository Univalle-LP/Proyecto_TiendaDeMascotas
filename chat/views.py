from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
import logging
from django.utils.timezone import now
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum, Q

from .models import Chat, MensajeChat  # Asume que estos modelos están definidos
from usuarios.models import Usuario    # Asume que este modelo está definido
from productos.models import Producto, Categoria  # Asume que estos modelos están definidos
from ventas.models import VentaDetalle  # Asume que este modelo está definido

# Auditoría
try:
    from auditoria.utils import registrar_auditoria_actualizar
except ImportError:
    registrar_auditoria_actualizar = None

# Gemini 2.5 imports
try:
    from google import genai
    from google.genai.errors import APIError
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    # Si no está disponible, crear stubs
    class APIError(Exception):
        pass
    class genai:
        class Client:
            def __init__(self, api_key=None):
                pass
        @staticmethod
        def Client(**kwargs):
            return None

logger = logging.getLogger(__name__)

# Crear cliente Gemini 2.5
# Asegúrate de que settings.GEMINI_API_KEY esté configurado en settings.py

client = None
if GEMINI_AVAILABLE:
    try:
        client = genai.Client(api_key="AIzaSyA7MsTs9K6VZJVOpjdxPi5oY9snaO5fZ3c")
        print("Inicializando cliente Gemini 2.5...")
        logger.info("Cliente Gemini 2.5 inicializado correctamente.")
    except Exception as e:
        # Manejo básico si la clave no está disponible al inicio
        logger.error(f"Error al inicializar Gemini: {e}")
        client = None
else:
    logger.warning("Google Generative AI no está instalado. El chat funcionará en modo limitado.")

# ===========================
# FUNCIONES AUXILIARES
# ===========================

def chat_widget(request):
    """Renderiza el fragmento del widget de chat."""
    try:
        return render(request, 'chat/widget.html')
    except Exception:
        return JsonResponse({'ok': False, 'error': 'widget template not found'}, status=404)


def get_user_data(user_id):
    """Obtiene datos de usuario usando SQL directo."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre, email FROM usuarios_usuario WHERE id = %s", [user_id])
        row = cursor.fetchone()
        if row:
            return {"nombre": row[0], "email": row[1]}
        return None


def get_categories():
    logger.debug("Obteniendo categorías de productos...")
    """Obtiene categorías de productos usando SQL directo."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre FROM productos_categoria ORDER BY nombre LIMIT 6")
        return [row[0] for row in cursor.fetchall()]


def get_top_products():
    """Obtiene los productos con mayor stock usando SQL directo."""
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT nombre FROM productos_producto WHERE estado = 'activo' AND stock_actual > 0 ORDER BY stock_actual DESC LIMIT 6"
        )
        return [row[0] for row in cursor.fetchall()]


def get_gemini_response(prompt, history=[]):
    """
    Genera una respuesta usando la API Gemini 2.5, incluyendo el historial.
    
    El historial debe ser una lista de {'role': 'Usuario'/'Bot', 'text': '...'}
    """
    if not client:
        return "El asistente inteligente no está disponible debido a un error de configuración."

    try:
        # 1. Instrucción de sistema para el modelo
        system_instruction = (
            "Eres Adonai, un asistente de chat amigable y profesional para una tienda de Mascotas. "
            "Tu rol principal es ayudar con pedidos, productos, promociones, delivery e información de contacto. "
            "\n\n"
            "CONTEXTO IMPORTANTE - TEORÍA DE COLAS M/M/1:\n"
            "- Estás gestionando una cola de atención personalizada con un único servidor (M/M/1)\n"
            "- Los clientes se atienden por orden de PRIORIDAD y hora de llegada (FIFO)\n"
            "- Prioridad 3 (URGENTE): Reclamos, problemas, solicitudes urgentes\n"
            "- Prioridad 2 (IMPORTANTE): Pedidos, compras, órdenes\n"
            "- Prioridad 1 (NORMAL): Consultas generales\n"
            "- El sistema registra automáticamente:\n"
            "  * Hora de llegada del cliente (λ - tasa de llegada)\n"
            "  * Tiempo de atención (μ - tasa de servicio)\n"
            "  * Posición en cola (Lq - clientes esperando)\n"
            "  * Tiempo de espera promedio (Wq)\n"
            "  * Tiempo total en sistema (Ws)\n"
            "\n"
            "INSTRUCCIONES DE RESPUESTA:\n"
            "- Mantén respuestas concisas y claras\n"
            "- Si el cliente tiene un RECLAMO o PROBLEMA, muestra empatía e intenta resolver rápidamente\n"
            "- Para consultas de PEDIDOS, proporciona información relevante\n"
            "- Para otros temas, sé amable y útil\n"
            "- El historial de conversación es importante - mantén la conversación contextualizada\n"
            "- Este es un chat de ATENCIÓN PERSONALIZADA, así que trata al cliente como si fuera tu prioridad\n"
        )
        
    
        # 2. Construir la estructura de 'contents' para la API de Gemini
        contents = []
        
        # Agregar el historial
        for message in history:
            # Gemini espera 'user' o 'model' (que representa al bot) como roles
            role = 'user' if message['role'] == 'Usuario' else 'model'
            contents.append({'role': role, 'parts': [{'text': message['text']}]})
            
        # Agregar el mensaje actual del usuario (el prompt)
        contents.append({'role': 'user', 'parts': [{'text': prompt}]})
        
        # 3. Llamar a la API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents, # Se envía el historial completo
            config={"system_instruction": system_instruction}
        )
        
        return response.text.strip() if response and response.text else "No pude generar una respuesta."
        
    except APIError as e:
        logger.error(f"Error en Gemini API (APIError): {e}")
        return "Hubo un problema al conectar con el asistente inteligente. Por favor, inténtalo de nuevo."
    except Exception as e:
        logger.error(f"Error en Gemini API: {e}")
        return "Hubo un problema desconocido al procesar tu solicitud."


# ===========================
# VISTA PRINCIPAL DEL CHAT
# ===========================

@csrf_exempt
def chat_send(request):
    """Endpoint POST que recibe {'message': '...'} o {'option': '...'} y devuelve la respuesta del bot."""
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        logger.error(f"Error al parsear JSON: {e}")
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    message = (payload.get('message') or '').strip()
    option = payload.get('option')
    usuario_id = payload.get('usuario_id')

    if not message and not option:
        return JsonResponse({'ok': False, 'error': 'Mensaje vacío'}, status=400)

    # Obtener o crear chat
    chat = None
    if usuario_id:
        try:
            # Usar .select_related() para evitar consultas N+1 si el modelo Chat accede a Usuario
            user = Usuario.objects.get(pk=usuario_id)
            
            # Primero, buscar un chat activo (esperando o en_atencion)
            chat = Chat.objects.filter(
                usuario=user,
                estado__in=['esperando', 'en_atencion']
            ).first()
            
            # Si no hay chat activo, crear uno nuevo
            if not chat:
                chat = Chat.objects.create(
                    usuario=user,
                    estado='en_atencion',
                    prioridad=1,
                    llegada=timezone.now()
                )
            logger.debug(f"Chat obtenido/creado: {chat.id}, Estado: {chat.estado}")
        except Usuario.DoesNotExist:
            logger.error(f"Usuario {usuario_id} no encontrado")
            chat = None
        except Exception as e:
            logger.error(f"Error al obtener/crear chat: {e}")
            chat = None

    user_text = option if option else message
    reply = None
    suggested = []
    
    # Si es una respuesta de la lógica interna, guardar mensaje del usuario AHORA
    # Si es para Gemini (else), lo guardamos MÁS TARDE para asegurar que el historial sea preciso.
    is_internal_reply = False 

    text_lower = (user_text or '').lower()

    # ===========================
    # LÓGICA INTERNA DEL BOT (Respuestas rápidas y estructuradas)
    # ===========================
    if option:
        opt_lower = str(option).lower()
        is_internal_reply = True 

        if 'product' in opt_lower or 'producto' in opt_lower or 'productos' in opt_lower or 'categor' in opt_lower:
            try:
                cats = list(Categoria.objects.order_by('nombre')[:6].values_list('nombre', flat=True))
            except Exception:
                cats = []
            
            if cats:
                reply = 'Selecciona una categoría o escribe el nombre del producto que buscas:'
                suggested = list(cats)
            else:
                reply = 'No hay categorías disponibles. Escribe el nombre del producto que buscas.'
                suggested = []
        
        elif 'promoc' in opt_lower:
            reply = 'Revisa nuestra sección de promociones en la web. Aquí solo te daré un recordatorio.'
            suggested = []

        elif 'delivery' in opt_lower or 'domicilio' in opt_lower:
            try:
                available = Producto.objects.filter(estado='activo', stock_actual__gt=0).exists()
            except Exception:
                available = False
                
            if available:
                reply = 'Sí, hacemos delivery. Indica tu ciudad para confirmar disponibilidad.'
            else:
                reply = 'Por ahora no hay productos disponibles para delivery.'
            suggested = []

        elif 'inform' in opt_lower or 'horario' in opt_lower or 'contacto' in opt_lower:
            reply = 'Nuestro horario es Lunes a Domingo 9:00-22:00. Puedes contactarnos al +123456789.'
            suggested = []

    # ===========================
    # SALUDOS Y RESPUESTAS BÁSICAS (Por texto o por opción simple)
    # ===========================
    elif text_lower in ('hola', 'buenas', 'buenos dias', 'buenas tardes') or text_lower.startswith('hola'):
        is_internal_reply = True 
        reply = (
            '¡Buenos días! 👋\n'
            'Soy el asistente de Adonai. Puedo ayudarte con pedidos, productos, promociones y delivery.\n'
            'Elige una opción para comenzar:'
        )
        suggested = ['Productos', 'Categorías', 'Delivery', 'Información', 'Promociones']

    elif 'pedido' in text_lower:
        is_internal_reply = True 
        reply = 'Para consultarte el estado del pedido necesito tu número de pedido. Por favor escríbelo.'
        suggested = []
    
    elif 'lo mas vendido' in text_lower or 'mas vendido' in text_lower or 'top' in text_lower:
        is_internal_reply = True 
        try:
            top_qs = (VentaDetalle.objects.values('producto__nombre')
                      .annotate(total_cantidad=Sum('cantidad'))
                      .order_by('-total_cantidad')[:5])
            top_list = [f"{t['producto__nombre']} ({t['total_cantidad']} vendidas)" for t in top_qs]
        except Exception:
            top_list = []
            
        if top_list:
            reply = 'Lo más vendido ahora:'
            suggested = top_list
        else:
            reply = 'Aún no hay datos de ventas para mostrar lo más vendido.'
            suggested = []

    elif 'delivery' in text_lower or 'domicilio' in text_lower:
        is_internal_reply = True 
        try:
            available = Producto.objects.filter(estado='activo', stock_actual__gt=0).exists()
        except Exception:
            available = False
            
        if available:
            reply = 'Sí, hacemos delivery. Indica tu ciudad para confirmar disponibilidad.'
        else:
            reply = 'Por ahora no hay productos disponibles para delivery.'
        suggested = []

    else:
        # 🧠 Respuesta inteligente con Gemini 2.5 (Si no cae en ninguna regla interna)
        
        # 1. Obtener historial (últimos 9 mensajes ANTERIORES)
        history_for_gemini = []
        if chat:
            # Se obtienen los últimos 9 mensajes, ordenados de más antiguo a más reciente
            recent_messages_qs = MensajeChat.objects.filter(chat=chat).order_by('-fecha_envio')[:9]
            # Invertir la lista para orden cronológico (de antiguo a nuevo)
            recent_messages = list(reversed(recent_messages_qs))
            
            history_for_gemini = [
                {'role': msg.remitente, 'text': msg.contenido} 
                for msg in recent_messages
            ]

        # 2. Llamar a la función Gemini con el historial
        reply = get_gemini_response(user_text, history=history_for_gemini)
        suggested = []


    # ===========================
    # GUARDAR MENSAJES Y RESPONDER
    # ===========================
    
    # 1. Guardar mensaje del usuario (solo si el chat existe)
    if chat:
        try:
            # Solo se crea si no fue creado antes por un camino de lógica interna
            if is_internal_reply:
                 MensajeChat.objects.get_or_create(
                     chat=chat, 
                     remitente='Usuario', 
                     contenido=user_text,
                     defaults={'chat': chat, 'remitente': 'Usuario'}
                 )
            else:
                 # Si vino por Gemini, el mensaje del usuario no se ha guardado
                 MensajeChat.objects.create(
                     chat=chat, 
                     remitente='Usuario', 
                     contenido=user_text
                 )
            logger.debug(f"Mensaje del usuario guardado: {user_text}")
        except Exception as e:
            logger.error(f"Error al guardar mensaje del usuario: {e}")

    # 2. Guardar respuesta del bot (solo si el chat existe y hay una respuesta)
    if chat and reply:
        try:
            MensajeChat.objects.create(
                chat=chat, 
                remitente='Bot', 
                contenido=reply
            )
            logger.debug(f"Respuesta del bot guardada")
        except Exception as e:
            logger.error(f"Error al guardar mensaje del bot: {e}")

    logger.debug(f"Usuario ID: {usuario_id}, Mensaje: {message}, Opción: {option}")
    logger.debug(f"Respuesta del bot: {reply}, Opciones sugeridas: {suggested}")

    # Si no hay respuesta, devolver un mensaje de error
    if not reply:
        logger.error(f"No se generó respuesta para el usuario {usuario_id}")
        reply = "Disculpa, hubo un problema al procesar tu mensaje. Por favor, intenta de nuevo."

    return JsonResponse({'ok': True, 'reply': reply, 'suggested': suggested})


# ===========================
# ATENCIÓN PERSONALIZADA (M/M/1)
# ===========================

def asignar_prioridad(texto):
    """Asigna prioridad basada en palabras clave del mensaje."""
    texto = texto.lower()
    if "urgente" in texto or "reclamo" in texto or "problema" in texto:
        return 3
    elif "pedido" in texto or "compra" in texto or "orden" in texto:
        return 2
    else:
        return 1


def procesar_cola():
    """
    Procesa la cola M/M/1 (un único servidor).
    Si hay un chat esperando y el servidor está libre, atiéndelo.
    Retorna el siguiente chat a atender o None.
    """
    # Si ya hay un chat en atención, no atender otro (1 servidor)
    if Chat.objects.filter(estado='en_atencion').exists():
        return None

    # Buscar siguiente en cola por prioridad (mayor primero) y hora de llegada (FIFO)
    siguiente = Chat.objects.filter(estado='esperando').order_by('-prioridad', 'llegada').first()

    if siguiente:
        siguiente.estado = 'en_atencion'
        siguiente.inicio_servicio = timezone.now()
        siguiente.save()
        # 📝 Registrar cambio de estado en auditoría
        if registrar_auditoria_actualizar:
            try:
                registrar_auditoria_actualizar(
                    usuario=siguiente.usuario,
                    entidad='Solicitud (Chat)',
                    nombre_objeto=f'Chat #{siguiente.id}',
                    cambios='Estado: esperando -> en_atencion'
                )
            except Exception as e:
                logger.error(f"Error registrando auditoría de chat: {e}")
        return siguiente
    return None


@csrf_exempt
def chat_personalizado(request):
    """
    Endpoint para atención personalizada con cola M/M/1.
    
    POST /chat/personalizado/
    {
        "usuario_id": 1,
        "message": "Quiero atención personalizada"
    }
    
    Responde:
    {
        "ok": true,
        "reply": "Has sido agregado a la cola...",
        "posicion": 2,
        "estado": "esperando"
    }
    """
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    usuario_id = payload.get('usuario_id')
    mensaje = (payload.get('message') or '').strip()

    if not mensaje:
        return JsonResponse({'ok': False, 'error': 'Mensaje vacío'}, status=400)

    # Si no hay usuario_id, intentar obtener del usuario autenticado en la sesión
    if not usuario_id and request.user.is_authenticated:
        usuario_id = request.user.id

    if not usuario_id:
        return JsonResponse({'ok': False, 'error': 'Usuario no autenticado. Por favor, inicia sesión.'}, status=403)

    try:
        user = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)

    # Verificar si el usuario ya tiene un chat activo (esperando o en atención)
    chat_activo = Chat.objects.filter(
        usuario=user,
        estado__in=['esperando', 'en_atencion']
    ).first()

    if chat_activo:
        # Usar el chat existente
        chat = chat_activo
        nueva_entrada = False
    else:
        # Crear nuevo chat con estado "esperando"
        prioridad = asignar_prioridad(mensaje)
        chat = Chat.objects.create(
            usuario=user,
            estado='esperando',
            prioridad=prioridad,
            llegada=timezone.now()
        )
        nueva_entrada = True

    # Guardar mensaje del usuario
    MensajeChat.objects.create(
        chat=chat,
        remitente='Usuario',
        contenido=mensaje
    )

    # Procesar la cola M/M/1
    siguiente = procesar_cola()
    
    # Refrescar el estado del chat desde la BD por si procesar_cola lo cambió
    chat.refresh_from_db()

    # Determinar respuesta según el estado
    if chat.estado == 'en_atencion':
        # Este chat está siendo atendido ahora
        reply = (
            "🎧 ¡Tu turno ha llegado! Iniciando atención personalizada...\n"
            "Un momento mientras te conectamos con el asistente.\n"
            "Cuéntame, ¿en qué te puedo ayudar?"
        )
        estado_chat = 'en_atencion'
        posicion = 0
    else:
        # El chat sigue en la cola
        posicion = Chat.objects.filter(
            estado='esperando',
            llegada__lt=chat.llegada
        ).count() + 1

        if posicion == 1:
            reply = (
                "📋 Has sido agregado a la cola de atención personalizada.\n"
                "¡Eres el siguiente! Tu turno comenzará en breve."
            )
        else:
            reply = (
                f"📋 Has sido agregado a la cola de atención personalizada.\n"
                f"Hay {posicion - 1} cliente(s) antes que tú. Tu turno llegará pronto."
            )
        estado_chat = 'esperando'

    # Guardar respuesta del bot
    MensajeChat.objects.create(
        chat=chat,
        remitente='Bot',
        contenido=reply
    )

    return JsonResponse({
        'ok': True,
        'reply': reply,
        'posicion': posicion,
        'estado': estado_chat,
        'chat_id': chat.id,
        'suggested': []
    })