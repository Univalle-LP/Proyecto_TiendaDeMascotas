# Contribuyendo al Proyecto

¡Gracias por tu interés en contribuir a **Tienda de Mascotas**! Este documento te guiará a través del proceso.

---

## 🎯 Antes de Comenzar

### Obtén Acceso

1. Fork el repositorio
2. Clona tu fork localmente
3. Agrega el remote upstream
   ```bash
   git remote add upstream https://github.com/Univalle-LP/Proyecto_TiendaDeMascotas.git
   ```

### Configuración Inicial

```bash
# Clona tu fork
git clone https://github.com/TU_USUARIO/Proyecto_TiendaDeMascotas.git
cd Proyecto_TiendaDeMascotas

# Crea entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instala dependencias
pip install -r requirements.txt

# Copia .env
cp .env.example .env

# Ejecuta migraciones
python manage.py migrate

# Crea usuario de prueba
python manage.py createsuperuser
```

---

## 📋 Selecciona una Tarea

### Opciones

1. **Issues abiertos**: Busca en [Issues](../../issues) con label `good first issue`
2. **Tu propia idea**: Crea un issue primero describiendo qué quieres hacer
3. **Roadmap público**: Revisa issues con label `enhancement`

### Antes de Trabajar

**SIEMPRE**:
```
1. Comenta en el issue: "Trabajaré en esto"
2. Asígnate el issue
3. Crea una rama basada en main
```

---

## 🔧 Desarrollo

### Estructura del Código

```
Proyecto_TiendaDeMascotas/
├── adonai/              # Configuración Django
├── usuarios/            # App de usuarios
├── productos/           # App de productos
├── pagos/              # App de pagos
├── chat/               # App de chat
├── auditoria/          # App de auditoría
├── venv/               # Entorno virtual
├── manage.py           # Script de Django
├── requirements.txt    # Dependencias
└── README.md           # Este archivo
```

### Estilo de Código

Seguimos:
- **PEP 8** para Python
- **Black** para formateo
- **Flake8** para linting

**Verifica tu código**:
```bash
black .
flake8 .
```

### Commits

**Formato de mensaje**:
```
tipo(scope): descripción

Descripción más larga si es necesario
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corregir bug
- `docs`: Documentación
- `style`: Formato, sin cambios de lógica
- `refactor`: Refactorizar sin cambios de comportamiento
- `test`: Tests
- `chore`: Cambios en build, deps, etc.

**Ejemplos**:
```bash
git commit -m "feat(auditoría): agregar registro de DELETE"
git commit -m "fix(pagos): corregir validación de cupones"
git commit -m "docs: actualizar README"
```

### Ramas

**Nombre de rama**:
```
<tipo>/<descripción>

tipo: feature, bugfix, hotfix, refactor, docs

Ejemplos:
feature/sistema-auditoría
bugfix/validacion-cupones
hotfix/crash-dashboard
```

**Crear rama**:
```bash
git checkout -b feature/tu-funcionalidad
# Basada en main
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test usuarios.tests.test_views

# Con cobertura
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML
```

### Escribir Tests

**Ubicación**: `app_name/tests/`

**Estructura**:
```python
from django.test import TestCase, Client
from usuarios.models import Usuario

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre="Test User",
            email="test@test.com"
        )
    
    def test_login_exitoso(self):
        response = self.client.post('/usuarios/login/', {
            'email': 'test@test.com',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_login_fallido(self):
        response = self.client.post('/usuarios/login/', {
            'email': 'wrong@test.com',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)  # Vuelve a mostrar form
```

**Cobertura mínima**: 80%

---

## 📝 Documentación

### Docstrings

```python
def registrar_auditoria(usuario, accion, entidad, descripcion):
    """
    Registra una acción de usuario en el AuditLog.
    
    Args:
        usuario (Usuario): Usuario que realizó la acción
        accion (str): Tipo de acción (CREATE, UPDATE, DELETE, etc)
        entidad (str): Nombre de la entidad afectada
        descripcion (str): Descripción detallada de la acción
    
    Returns:
        AuditLog: Instancia creada o None si hubo error
    
    Raises:
        ValidationError: Si los parámetros son inválidos
    """
    # implementación
```

### Comentarios

```python
# ✓ Buen comentario: explica el "por qué"
# Si el stock es negativo, significa que se debe pedir más
if producto.stock < 0:
    notificar_reorden(producto)

# ✗ Mal comentario: dice lo obvio
# Incrementar contador
contador += 1
```

### Archivos README

Si agregaste una app nueva, crea `app_name/README.md`:
```markdown
# Nombre de App

## Descripción
Qué hace esta app

## Modelos
- Modelo 1
- Modelo 2

## Vistas
- Vista 1
- Vista 2

## Endpoints
GET /app/endpoint/ - Descripción
POST /app/endpoint/ - Descripción
```

---

## 🔐 Seguridad

### Verificaciones de Seguridad

- [ ] No hay credenciales hardcodeadas
- [ ] Se validan todos los inputs del usuario
- [ ] Se usa parametrización en queries SQL (ORM)
- [ ] Se implementa CSRF protection
- [ ] Se hashean contraseñas correctamente
- [ ] Se logean acciones de seguridad

### Cómo Reportar Vulnerabilidades

**NO** abras issue público. En su lugar:

1. Email a: `security@example.com` (cuando exista)
2. Describe la vulnerabilidad
3. Incluye pasos para reproducir
4. Espera confirmación antes de publicar

---

## 🚀 Abriendo un Pull Request

### Checklist Antes de Abrir PR

- [ ] Tests escritos y pasan (`pytest` o `python manage.py test`)
- [ ] Código formateado (`black .`)
- [ ] Linter pasa (`flake8 .`)
- [ ] Documentación actualizada
- [ ] Commits con mensajes claros
- [ ] Rama actualizada con main (`git rebase origin/main`)
- [ ] Sin conflictos de merge

### Abriendo el PR

1. Empuja tu rama: `git push origin feature/tu-funcionalidad`
2. Ve a GitHub y abre un PR
3. Completa el **PULL_REQUEST_TEMPLATE.md** enteramente
4. Solicita 2+ reviewers
5. Vincula el issue

### Ejemplo de PR Bien Hecho

```markdown
## 📝 Descripción
Agrego sistema de auditoría para registrar eliminaciones de productos.

## 🔗 Issue Relacionado
Closes #42

## 🎯 Cambios Principales
- Agregada función `registrar_auditoria_eliminar()`
- Integrada en `producto_delete()` y `categoria_delete()`
- Tests añadidos con 85% coverage

## 📸 Evidencias
Tests pasando: ✓
Coverage 85%: ✓

## ✅ Checklist
- [x] Tests escritos
- [x] Documentación actualizada
- [x] Código pasa linter
```

---

## 👥 Revisión de Código

### Como Autor

**Durante la revisión**:
- Responde todos los comentarios
- Haz cambios si es necesario
- Comunica si estás en desacuerdo (respetuosamente)
- Pide help si algo no es claro

**Código de conducta**:
```
✓ "Buen punto, lo cambio"
✓ "Pregunta: ¿por qué sugieres eso?"
✗ "No voy a cambiar esto"
✗ "Es tu problema"
```

### Como Reviewer

**Busca**:
- ✓ Código correcto y funciona
- ✓ Sigue estándares del proyecto
- ✓ Tiene tests adecuados
- ✓ Documentación clara
- ✓ Sin vulnerabilidades de seguridad

**Comentarios útiles**:
```
✓ "Sugerencia: podrías usar ORM para evitar SQL injection"
✓ "Pregunta: ¿qué pasa si X?"
✓ "Buen test, pero falta el edge case Y"
✗ "Esto apesta"
✗ "Malo"
```

---

## 🎓 Convenciones del Proyecto

### Base de Datos

- **Nombres**: snake_case
- **Índices**: En campos frecuentemente buscados
- **Migraciones**: Un cambio por migración

### Frontend

- **JavaScript**: Vanilla JS (sin frameworks)
- **CSS**: Bootstrap 5
- **Validación**: Server-side + client-side

### Backend

- **Python**: 3.10+
- **Django**: 5.2+
- **ORM**: Django ORM (no SQL directo)
- **API**: RESTful cuando sea posible

### Auditoría

- **Cada cambio CRUD se registra**
- **Usuario y timestamp obligatorios**
- **Descripción clara del cambio**

---

## 📚 Recursos Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Commits](https://www.conventionalcommits.org/)

---

## ❓ Ayuda

### Si tienes preguntas

1. Revisa issues cerrados relacionados
2. Busca en la documentación
3. Pregunta en el issue abierto
4. Contacta al equipo

### Problemas Comunes

**Conflicto de merge**:
```bash
git fetch origin
git rebase origin/main
# Resuelve conflictos
git add .
git rebase --continue
git push origin rama --force-with-lease
```

**Tests fallan localmente**:
```bash
# Limpia la BD de prueba
python manage.py flush

# Corre migraciones de nuevo
python manage.py migrate

# Reintenta tests
python manage.py test
```

**Linter falla**:
```bash
# Formatea automáticamente
black .

# Verifica issues
flake8 .

# Arregla manualmente si es necesario
```

---

## 🏆 Reconocimiento

Todos los contribuyentes son mencionados en:
- `CONTRIBUTORS.md`
- README.md
- Release notes

---

## 📋 Código de Conducta

Nos comprometemos a proporcionar un ambiente inclusivo y respetuoso.

**Esperamos**:
- ✓ Sé respetuoso con otros contribuyentes
- ✓ Acepta crítica constructiva
- ✓ Enfócate en el código, no en la persona
- ✓ Ayuda a otros cuando puedas

**Inaceptable**:
- ✗ Acoso o discriminación
- ✗ Ataques personales
- ✗ Contenido ofensivo
- ✗ Spam

---

¡Gracias por contribuir! 🎉

**Última actualización**: 2026-06-20
