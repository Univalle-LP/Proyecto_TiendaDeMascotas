from rest_framework import serializers

from .models import Categoria, Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'stock_actual',
            'categoria',
            'imagen',
        ]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'descripcion',
        ]
