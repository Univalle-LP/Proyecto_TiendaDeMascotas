from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'entidad', 'fecha_hora')
    list_filter = ('accion', 'entidad', 'fecha_hora')
    search_fields = ('usuario__nombre', 'entidad', 'descripcion')
    ordering = ('-fecha_hora',)
    readonly_fields = ('usuario', 'fecha_hora', 'accion', 'entidad', 'descripcion')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False
