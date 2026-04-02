🏥 Sistema de Gestión Clínica (CLI)

Sistema backend desarrollado en Python para la gestión de una clínica mediante una interfaz de consola (CLI). Permite manejar usuarios con distintos roles (paciente, médico, enfermero) y administrar citas, historiales médicos, tratamientos, facturación y más.

📌 Descripción

Este sistema simula el funcionamiento de una clínica real, integrando múltiples módulos que interactúan entre sí:

Autenticación de usuarios

Gestión de pacientes

Gestión de médicos y especialidades

Agendamiento de citas

Historial clínico

Tratamientos médicos

Facturación

Gestión de EPS

Todo el flujo se maneja desde consola mediante menús interactivos según el rol del usuario.

👥 Roles del sistema
🧑‍🦱 Paciente

Ver y actualizar su perfil

Registrar sus datos

Consultar EPS

Agendar, actualizar y eliminar citas

Generar facturas

🧑‍⚕️ Médico

Ver citas asignadas

Gestionar historial médico

Registrar, actualizar y eliminar médicos

Gestionar especialidades

👩‍⚕️ Enfermero

Registrar enfermeros

Consultar enfermeros

Actualizar observaciones en historial clínico

⚙️ Funcionalidades principales

🔐 Login y registro de usuarios con roles

📅 CRUD completo de citas

📋 CRUD de historial médico

💊 Gestión de tratamientos

🧾 Generación de facturas

🏥 Gestión de EPS

👨‍⚕️ Relación médico–especialidad

🧑‍🦱 Relación paciente–usuario

🧠 Tecnologías utilizadas

Python

SQLAlchemy (ORM)

PostgreSQL (Neon DB)

UUID para identificación única

Arquitectura modular (CRUD + Entities)

📂 Estructura del proyecto
src/
│
├── database/
│   └── config.py
│
├── entities/              # Modelos de base de datos
│   ├── usuario.py
│   ├── paciente.py
│   ├── medico.py
│   ├── cita.py
│   ├── historial.py
│   ├── tratamiento.py
│   ├── eps.py
│   ├── enfermero.py
│   └── factura.py
│
├── crud/                  # Lógica de negocio
│   ├── crud_usuario.py
│   ├── crud_paciente.py
│   ├── crud_medico.py
│   ├── crud_cita.py
│   ├── crud_historial.py
│   ├── crud_tratamiento.py
│   ├── crud_eps.py
│   ├── crud_enfermero.py
│   └── crud_factura.py
│
└── main.py                # Interfaz de consola (CLI)
🚀 Ejecución del proyecto

Clonar repositorio:

git clone <URL_DEL_REPO>
cd <NOMBRE_PROYECTO>

Crear entorno virtual:

python -m venv venv
venv\Scripts\activate  # Windows

Instalar dependencias:

pip install -r requirements.txt

Configurar base de datos (.env):

DATABASE_URL=postgresql://user:password@host/db

Ejecutar:

python main.py
🧩 Flujo del sistema

Si no existen usuarios → se crea el primero

Login del usuario

Acceso al sistema según rol:

Paciente → menú de paciente

Médico → menú de médico

Enfermero → menú de enfermería

📊 Presentación del proyecto

Puedes ver la presentacion de integracion de los endpoints con FastAPI aquí:

👉 https://canva.link/5wp5qqmdbqik1vk

Puedes ver la presentación del ORM aquí:

👉 https://www.canva.com/design/DAHEaazGp9A/znY5bCsAEHZoLc5cEYlbPA/edit?utm_content=DAHEaazGp9A&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


🧪 Validaciones implementadas

Verificación de UUID

Campos obligatorios

Validación de formatos de fecha

Control de duplicados (facturas, EPS, etc.)

Restricción de acciones según usuario

📌 Notas técnicas

El sistema utiliza datetime con zona horaria UTC

Las relaciones entre entidades están normalizadas

Separación en capas:

entidades (modelo)

lógica (CRUD)

interfaz (main)

💡 Posibles mejoras

Interfaz gráfica (GUI o web con Flask/Django)

Autenticación con tokens (JWT)

Control de permisos más robusto

API REST

Reportes y estadísticas