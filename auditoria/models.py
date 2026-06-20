from django.db import models
from usuarios.models import Usuario


class AuditLog(models.Model):
    """
    Modelo para registrar todas las acciones realizadas por los usuarios en el sistema.
    """
    ACCIONES_CHOICES = (
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('VIEW', 'Visualización'),
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
        ('ERROR', 'Error'),
        ('OTHER', 'Otro'),
    )

    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=20, choices=ACCIONES_CHOICES)
    entidad = models.CharField(max_length=100, help_text="Nombre del modelo/tabla afectada (ej: Usuario, Producto, Venta)")
    descripcion = models.TextField(help_text="Descripción detallada de la acción realizada")

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-fecha_hora']
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        indexes = [
            models.Index(fields=['usuario', '-fecha_hora']),
            models.Index(fields=['accion', '-fecha_hora']),
            models.Index(fields=['entidad', '-fecha_hora']),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} en {self.entidad} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')})"
