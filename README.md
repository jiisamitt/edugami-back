# Prueba técnica

¡Hola, bienvenido a mi proyecto! Intentaré explicar brevemente los detalles a considerar para que puedan revisarlo de manera sencilla.

## 1. Consideraciones generales

El proyecto contiene todo lo pedido en el documento, pero con algunas suposiciones en algunos de los requests. Se asume que no se utiliza ningún tipo de autenticación ni complejidades adicionales.

## 2. Consideraciones específicas

### Modelos

Asumí que no importaba mucho el nombre de `tagType` o `axisType`, ya que en las semillas se menciona `axisType`, pero en los modelos se tiene `tagType`.

### Despliegue

La aplicación está desplegada en un servicio gratis, por lo que para hacer cualquier request se debe esperar alrededor de 30-60 segundos despues del primer request, ya que se encuentra "congelado". Una vez que funciona el primero, se puede usar con más normalidad.

### /test

Para crear una prueba, asumí que el `id` viene dentro del request (para `student`, `test`, `question`, y `alternative`). En Django, generalmente no es una buena práctica (Django crea los `id` automáticamente), pero como en la semilla los incluyen, pensé que sería necesario para luego comparar.

Además, asumí que los `id` de las alternativas están incorrectos a partir de la segunda pregunta (empiezan nuevamente desde 1).

### /student (post)

Creé un endpoint para manejar estudiantes, aunque no se menciona explícitamente. Creo que es necesario para darle sentido al problema.

### /load-students (post)

Este endpoint permite crear varios estudiantes a la vez, como se requiere en la semilla proporcionada.

### /recommendations/<int:student-id> (get)

Este es una conexión simple con OpenAI, que genera recomendaciones dependiendo del score obtenido para cada `axis`. Si el estudiante obtiene un buen puntaje, le recomienda cosas más difíciles; si no, le sugiere ejercicios más sencillos.

Lo interesante es que se pueden agregar más detalles al prompt de manera sencilla para generar respuestas más precisas, adaptadas a las necesidades del estudiante.

Se puede guardar el progreso histórico del estudiante en cierto eje, felicitarlo, darle ánimos, o sugerir conceptos más básicos, por esto también era necesario crear el modelo estudiante.

### /reset (delete)

Este endpoint permite borrar rápidamente toda la base de datos, útil para pruebas.

## 3. Correr el proyecto

El proyecto está desplegado, pero en caso de querer ejecutarlo localmente, se necesita tener Python 3.x como mínimo. Se recomienda crear un entorno virtual (venv) e instalar todas las dependencias dentro de él. Los pasos serían los siguientes:

1. Clonar el repositorio.
2. Se puede crear una base de datos localmente (si tienen PostgreSQL), o conectarse a la base de datos que se utiliza en el proyecto (las variables de conexión deben ir en el archivo `.env` que deberán crear también y posicionarlo al mismo nivel de `manage.py`).
3. Posicionarse en el directorio donde está `manage.py`.
4. (Opcional y fuertemente recomendado) Crear un entorno virtual con el comando:

   ```bash
   python -m venv venv
   ```

5. (Opcional y fuertemente recomendado) Activar el entorno virtual:

   ```bash
   # En Windows
   venv\Scripts\activate

   # En macOS/Linux
   source venv/bin/activate
   ```

6. Instalar las dependencias con el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

7. Crear las migraciones:

   ```bash
   python manage.py makemigrations
   ```

8. Aplicar las migraciones a la base de datos:

   ```bash
   python manage.py migrate
   ```

9. Ejecutar el servidor local:

   ```bash
   python manage.py runserver
   ```
