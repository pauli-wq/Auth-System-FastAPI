
# Sistema de Autenticación con FastAPI

Una API REST desarrollada con **FastAPI** que proporciona funcionalidades de autenticación de usuarios con tokens JWT. Ideal para integrar en aplicaciones web o móviles que requieran control de acceso seguro.

## 🚀 Características

- Registro e inicio de sesión de usuarios.
- Protección de rutas con tokens JWT.
- Integración con base de datos usando SQLAlchemy.
- Seguridad con hashing de contraseñas usando el algoritmo **Argon2**.
- Validación de datos con Pydantic.

## 🛠️ Tecnologías Usadas

- *Python*
- *FastAPI*
- *SQLAlchemy*
- *Pydantic*
- *Pwdlib* (para hashing de contraseñas)
- *Uvicorn*

## 📦 Instalación

1. Clona el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-proyecto>
    ```
   
2. Crea un entorno virtual:

  ```bash
  python -m venv venv
  source venv/bin/activate  
  ```

3. Instala las dependencias: 

  ```bash
  pip install -r requirements.txt
  ```

