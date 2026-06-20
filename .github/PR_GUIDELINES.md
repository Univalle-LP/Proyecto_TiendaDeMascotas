# 🚀 Guía de Buenas Prácticas - Pull Requests

**Proyecto**: Tienda de Mascotas  
**Versión**: 1.0

---

## 📌 Antes de Crear el PR

### 1. Asegúrate de que tu rama está actualizada

```bash
git fetch origin
git rebase origin/main
# O si hay conflictos
git merge origin/main
```

### 2. Verifica que no hay código de debug

```bash
# Busca console.log, print(), debugger, etc
grep -r "console.log" src/
grep -r "print(" .
grep -r "debugger" src/
```

### 3. Ejecuta tests localmente

```bash
python manage.py test
npm test  # si hay frontend
```

### 4. Revisa tu propio código

```bash
git diff origin/main
# Verifica línea por línea
```

### 5. Asegúrate que el linter pase

```bash
flake8 .
black .
```

---

## ✍️ Escribiendo el PR

### Título del PR

**Formato**: `[TIPO] Descripción breve`

**Ejemplos correctos**:
```
[FEATURE] Agregar sistema de auditoría para DELETE
[BUG] Corregir validación de cupones expirados
[DOCS] Actualizar documentación de API
[REFACTOR] Simplificar lógica de pago Stripe
[HOTFIX] Arreglar crash en dashboard
```

**Ejemplos INCORRECTOS**:
```
✗ Fix bugs
✗ Update stuff
✗ Changes
✗ WIP
```

### Descripción

**Haz**:
- ✅ Sé específico: "Agregué validación para cupones vencidos"
- ✅ Explica el **por qué**: "Usuarios podían usar cupones expirados"
- ✅ Usa viñetas: "- Cambio 1\n- Cambio 2"
- ✅ Vincula issues: "Closes #123"

**No hagas**:
- ❌ Descripciones genéricas
- ❌ Cambios sin contexto
- ❌ PRs que hacen "todo"
- ❌ Olvidar de vincular issues

### Issue Relacionado

**Forma correcta**:
```
Closes #123
Closes #124, #125  # Múltiples
Related to #456
```

**Qué hace**:
- `Closes` → Cierra el issue automáticamente cuando merge
- `Related to` → Solo vincula sin cerrar

---

## 🎯 Evidencias

### Para cambios visuales

**Incluye**:
```
**Antes:**
[Captura 1]

**Después:**
[Captura 2]
```

### Para cambios en API

**Documenta**:
```
**Endpoint**: POST /api/nuevo/
**Parámetros**: 
{
  "param1": "value",
  "param2": 123
}
**Respuesta**:
{
  "id": 1,
  "status": "created"
}
```

### Para cambios de base de datos

**Incluye**:
```
**Migración**: 0001_initial.py
**Cambios en modelo**:
- Agregado campo: descripcion (TextField)
- Modificado campo: precio (decimal 10,2 → 12,4)
```

---

## 🧪 Testing

### Tests Unitarios

```python
# Debe incluir pruebas para:
- Caso exitoso
- Casos de error
- Edge cases

# Ejemplo:
def test_validar_cupon_expirado():
    cupon = Cupon.objects.create(
        codigo="VENCIDO",
        fecha_expira=date(2020, 1, 1)
    )
    resultado = validar_cupon("VENCIDO")
    assert resultado['valido'] == False
```

### Cobertura

```bash
coverage run --source='.' manage.py test
coverage report
# Mínimo 80% para código nuevo
```

---

## 🔄 Tipos de Cambios

### 🐛 BUG FIX

**Incluye**:
```
- Descripción del bug
- Pasos para reproducir
- Por qué ocurría
- Cómo se corrigió
```

**Ejemplo**:
```
## Problema
Usuario no podía cambiar contraseña si tenía caracteres especiales

## Reproducir
1. Login
2. Ir a /usuarios/cambiar-contrasena/
3. Escribir "P@ss123!" 
4. Error

## Causa
Falta validación en regex de contraseña

## Solución
Actualicé regex para permitir caracteres especiales: `[A-Za-z0-9!@#$%^&*]`
```

### ✨ FEATURE

**Incluye**:
```
- Qué nueva funcionalidad se agregó
- Por qué era necesaria
- Cómo se usa
- Ejemplos de código
```

**Ejemplo**:
```
## Funcionalidad
Sistema de auditoría para registrar eliminaciones

## Uso
Cuando un admin elimina un producto, se registra:
- Usuario
- Fecha/hora
- Entidad
- Detalles

## Ejemplo
DELETE /panel/inventario/15/eliminar/
→ Registra en audit_logs: "Admin eliminó Producto: Collar (stock bajo)"
```

### 📝 DOCUMENTATION

**Incluye**:
```
- Qué se documentó
- Cambios en documentación existente
- Links a documentación
```

### 🔄 REFACTOR

**Incluye**:
```
- Código antes/después (diff)
- Por qué se refactorizó
- Mejoras (performance, legibilidad)
```

---

## 🚫 Qué Evitar

### ❌ PRs Demasiado Grandes

**Problema**: Difícil de revisar, introduce muchos cambios

**Solución**: Divide en varios PRs
```
PR 1: [FEATURE] Modelo de auditoría
PR 2: [FEATURE] Auditoría para CREATE
PR 3: [FEATURE] Auditoría para UPDATE
PR 4: [FEATURE] Auditoría para DELETE
```

### ❌ PRs sin Tests

**Problema**: No se verifica que funciona

**Solución**: Siempre incluye tests
```
- [ ] Tests unitarios ✓
- [ ] Tests de integración ✓
- [ ] Coverage ≥ 80% ✓
```

### ❌ PRs sin Documentación

**Problema**: Difícil de mantener

**Solución**: Actualiza docs
```
- [ ] README actualizado ✓
- [ ] Docstrings agregados ✓
- [ ] API documentada ✓
```

### ❌ Cambios no relacionados

**Problema**: Mezcla cambios de distintos issues

**Solución**: Un PR = Un issue (generalmente)

### ❌ Commits poco claros

**Problema**: Mensaje "Update files"

**Solución**: Commits descriptivos
```bash
✓ git commit -m "feat: agregar validación de cupones expirados"
✓ git commit -m "fix: corregir error al eliminar productos"
✗ git commit -m "update"
✗ git commit -m "fix bug"
```

---

## 👥 Durante la Revisión

### Para el Autor

**Responde constructivamente**:
```
✓ "Entiendo, lo cambio para usar ORM en lugar de SQL directo"
✓ "Buen punto, agregaré test para ese edge case"
✗ "No, así está bien"
✗ "Ignoraré este comentario"
```

**Actualiza el PR si hay feedback**:
```bash
# Haz los cambios
git add .
git commit -m "refactor: actualizar según feedback de review"
git push origin mi-rama

# O fuerza push si reescribiste historia
git push origin mi-rama --force-with-lease
```

### Para el Reviewer

**Sé constructivo**:
```
✓ "Sugerencia: Podrías usar ORM para evitar SQL injection"
✓ "¿Consideraste este edge case?"
✗ "Esto es horrible"
✗ "Mal hecho"
```

---

## ✅ Checklist Final

Antes de hacer "push" y abrir el PR:

- [ ] Rama está actualizada (`git rebase origin/main`)
- [ ] Tests locales pasan (`pytest` o `python manage.py test`)
- [ ] Linter pasa (`flake8`, `black`)
- [ ] No hay código de debug
- [ ] Commits tienen mensajes claros
- [ ] Documentación está actualizada
- [ ] Evidencias adjuntadas (si aplica)
- [ ] Issue está vinculado
- [ ] PR explica claramente qué cambia
- [ ] Checklist en template está completo

---

## 🚀 Flujo Completo

```
1. Crear rama
   git checkout -b feature/mi-funcionalidad

2. Desarrollar
   - Hacer cambios
   - Ejecutar tests
   - Hacer commits

3. Antes de push
   - git rebase origin/main
   - Verificar tests
   - Verificar linter

4. Push a remoto
   git push origin feature/mi-funcionalidad

5. Abrir PR en GitHub
   - Llenar template completamente
   - Adjuntar evidencias
   - Solicitar reviewers

6. Durante review
   - Responder comentarios
   - Hacer cambios si es necesario
   - Push again si hay cambios

7. Approval y Merge
   - Esperar aprobación
   - Squash & Merge o Rebase & Merge
   - Borrar rama

8. Deployment
   - QA verifica en staging
   - Deploy a producción
   - Monitorear
```

---

## 📞 Ayuda & Recursos

### Si tienes dudas

1. Revisa PRs anteriores para ver ejemplos
2. Lee la guía de contribución (CONTRIBUTING.md)
3. Pregunta en el equipo antes de abrir PR

### Referencias

- [Template de PR](.github/PULL_REQUEST_TEMPLATE.md)
- [Documentación API](DOCUMENTACION_API.md)
- [Estructura del código](README.md)

---

## 📈 Métricas de Calidad

Buscamos:
- ✅ 80%+ test coverage
- ✅ 0 conflicts de merge
- ✅ 0 warnings de linter
- ✅ Descripción clara (2+ párrafos)
- ✅ Documentación actualizada

---

**Última actualización**: 2026-06-20  
**Mantener**: Equipo de Desarrollo
