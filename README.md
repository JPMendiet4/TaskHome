# Task Manager API (Django REST)

API para **gestionar tareas** (*homeworks*) y **asignarlas a usuarios**. Permite crear, listar, actualizar y eliminar lógicamente usuarios y tareas, con validaciones de negocio (ventana horaria, estados, unicidad de contacto) y **notificaciones por correo** cuando se crean/actualizan/eliminan tareas.

## Características

* CRUD de **Usuarios** y **Tareas** con Django REST Framework.
* **Asignación** de tareas a usuarios activos.
* **Estados** de tarea: `Creado (C)`, `En proceso (P)`, `Terminado (T)`.
* Validaciones:

  * Usuario **activo** para poder asignarle tareas.
  * Ventana horaria válida para la tarea (**06:00–18:00**).
  * Email y teléfono con formato y **unicidad**.
* **Notificaciones por correo**:

  * Al crear/actualizar/eliminar tarea (según serializer).
* **Serialización enriquecida** de tareas: estado legible y nombre corto del usuario.

## Tecnologías

* Python 3.x
* Django 4.x / Django REST Framework
* SQLite (por defecto, configurable)
* Email backend configurado vía `settings.py`

## Modelado

**User**

* `name`, `last_name`, `email`, `phone_number`
* `status` (bool, para soft delete)
* `active` (bool, debe estar en `True` para asignación de tareas)

**Homework**

* `title`, `description`
* `user` (FK a `User`, `on_delete=PROTECT`)
* `time` (ventana 06:00–18:00)
* `status` (`C`, `P`, `T`)

## Endpoints

Base: `/api/` (ajusta según tu `urls.py` de proyecto)

### Usuarios

* `POST /create-user/` — Crear usuario
* `GET  /read-user/` — Listar usuarios activos (`status=True`)
* `PUT  /update-user/<id>/` — Actualizar usuario (reemplazo)
* `PATCH /update-user/<id>/` — Actualización parcial
* `DELETE /delete-user/<id>/` — Eliminación lógica (`status=False`)

### Tareas

* `POST /create-tarea/` — Crear tarea (envía correo “nueva tarea”)
* `GET  /read-tarea/` — Listar tareas con estado `C`/`P` (ver nota técnica)
* `PUT  /update-tarea/<id>/` — Actualizar tarea (envía correo “tarea actualizada”)
* `PATCH /update-tarea/<id>/` — Actualización parcial (puede enviar correos según estado)
* `DELETE /delete-tarea/<id>/` — Eliminación lógica (envía correo “tarea eliminada”) *(ver nota técnica sobre estado)*

## Ejemplos de uso (cURL)

### Crear usuario

```bash
curl -X POST http://localhost:8000/api/create-user/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana",
    "last_name": "García",
    "email": "ana@example.com",
    "phone_number": "+57 300-123-4567",
    "active": true
  }'
```

### Crear tarea

```bash
curl -X POST http://localhost:8000/api/create-tarea/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Preparar informe",
    "description": "Informe semanal de métricas",
    "user": 1,
    "time": "09:30:00",
    "status": "C"
  }'
```

### Listar tareas (C/P)

```bash
curl http://localhost:8000/api/read-tarea/
```

**Respuesta de tarea (ejemplo)**

```json
{
  "id": 5,
  "title": "Preparar Informe",
  "description": "Informe semanal de métricas",
  "time": "09:30:00",
  "status": "Creado",
  "user": {
    "id": 1,
    "username": "Ana García"
  }
}
```

## Instalación y ejecución

1. Clona el repositorio.
2. Crea entorno virtual e instala dependencias:

   ```bash
   python -m venv env
   source env/bin/activate   # Linux/Mac
   # env\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
3. Migra la base de datos:

   ```bash
   python manage.py migrate
   ```
4. Configura variables de email (ver sección **Configuración**).
5. Ejecuta el servidor:

   ```bash
   python manage.py runserver
   ```

## Configuración

Por defecto se utiliza **SQLite**. Puedes cambiar la base en `settings.py`.

Para el **envío de correos**, define en `settings.py` o variables de entorno:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.tu_proveedor.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "tu_correo@dominio.com"
EMAIL_HOST_PASSWORD = "tu_password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> El serializer usa `settings.EMAIL_HOST_USER` y direcciones “[from@example.com](mailto:from@example.com)”/“[mi\_correo\_ejemplo@example.com](mailto:mi_correo_ejemplo@example.com)” en distintos puntos. Alinea todos los remitentes con `DEFAULT_FROM_EMAIL`.

## Reglas de validación destacadas

* **Usuario activo**: `active=True` para poder asignarle tareas.
* **Ventana horaria de tarea**: `06:00:00` a `18:00:00`.
* **Unicidad** de `email` y `phone_number` entre usuarios.
* **Estados válidos** de tarea: `C`, `P`, `T`.

## Notas técnicas & mejoras sugeridas

> *Estas observaciones buscan robustecer el código tal como está hoy:*

1. **Filtro de tareas en `HomeworkReadAPIView`:**
   `Homework.objects.filter(status='C' or 'P')` siempre filtra por `'C'`.
   **Sugerido:** `Homework.objects.filter(status__in=['C', 'P'])`.

2. **Soft delete en `HomeworkSerializer.delete`:**
   El campo `status` en `Homework` es `CharField`, pero el método lo cambia a `False`.
   **Opciones:**

   * Cambiar a un booleano `active`/`is_deleted` para soft delete.
   * O bien, usar un estado adicional (p.ej. `X = Eliminada`) y validarlo.

3. **`partial_update` de `HomeworkSerializer`:**

   * Asigna `instance.name` y `instance.last_name` (propios de `User`) en lugar de campos de `Homework`.
   * Para `user`, asigna `instance.phone_number`.
     **Sugerido:** Corregir mapeos a `instance.title`, `instance.time`, `instance.user`.

4. **Remitentes de correo consistentes:**
   Unificar el remitente (usar siempre `settings.DEFAULT_FROM_EMAIL`).

5. **`get_status_display`:**
   Django ya provee `instance.get_status_display()` al definir `choices`. No es necesario redefinirlo, salvo que quieras lógica adicional.

6. **Validación de unicidad con `UniqueConstraint`:**
   Para `email`/`phone_number` se puede reforzar a nivel DB con `UniqueConstraint` o `unique=True` en el modelo (si aplica a tu negocio).

7. **Respuestas de `DELETE` de usuarios/tareas:**
   Actualmente hacen soft delete y devuelven un mensaje; considera devolver también el `id`/`status` final para trazabilidad.



## Contribuir

1. Crea una rama: `git checkout -b feature/mi-mejora`
2. Commit: `git commit -m "feat: mejora X"`
3. Push: `git push origin feature/mi-mejora`
4. Abre un PR

## Licencia

MIT (ajústala si tu proyecto requiere otra).

---

¿Quieres que agregue una **colección de Postman** o ejemplos de **requests con JWT** si más adelante proteges los endpoints? También puedo entregarte un `.env.example` alineado con tu `settings.py`.
