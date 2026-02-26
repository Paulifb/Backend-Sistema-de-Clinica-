🏥 Sistema de Gestión de Citas Médicas
📌 Descripción

El Sistema de Gestión de Citas Médicas es una aplicación desarrollada en Python que permite administrar el registro de pacientes, médicos, enfermeros, citas médicas y facturación dentro de una clínica.

El sistema está basado en Programación Orientada a Objetos (POO), aplicando principios como encapsulamiento, tipado, composición y uso de estructuras dinámicas (listas).

🎯 Objetivo del Proyecto

Desarrollar un sistema que permita:

Registrar pacientes y profesionales de la salud.

Agendar y reprogramar citas médicas.

Gestionar asistencia de enfermería.

Generar facturas.

Consultar información relevante del sistema.

🏗️ Arquitectura del Sistema

El sistema está compuesto por 5 entidades principales:

1️⃣ Paciente

Representa a una persona que recibe atención médica.

Responsabilidades:

Almacenar información personal.

Proveer datos para citas y facturación.

2️⃣ Médico

Representa a un profesional de la salud encargado de diagnosticar pacientes.

Responsabilidades:

Emitir diagnósticos.

Atender citas médicas.

3️⃣ Enfermero

Representa al profesional encargado de la asistencia médica básica.

Responsabilidades:

Administrar medicamentos.

Brindar apoyo clínico.

4️⃣ Cita

Relaciona un paciente con un profesional en una fecha y hora específica.

Responsabilidades:

Programar citas.

Reprogramar citas.

Mostrar información detallada.

Asociar paciente y profesional.

Utiliza el módulo datetime para manejar fechas correctamente.

5️⃣ Factura

Representa el proceso de cobro por servicios médicos.

Responsabilidades:

Generar factura asociada a una cita.

Mostrar información de pago.

⚙️ Funcionalidades del Sistema

El menú principal permite:

Registrar paciente

Registrar médico

Registrar enfermero

Agendar cita

Mostrar información de citas

Reprogramar cita

Asistencia de enfermería

Información del profesional

Recibir diagnóstico del doctor

Mostrar información del paciente

Tramitar factura

Salir del sistema

🧠 Conceptos de POO Aplicados

✔ Encapsulamiento mediante atributos privados.

✔ Uso de @property.

✔ Composición (una cita contiene un paciente y un profesional).

✔ Tipado estático con anotaciones.

✔ Validación de datos.

✔ Manejo de fechas con datetime.

🗂️ Estructura del Proyecto
src/
 ├── entities/
 │    ├── Pacientes.py
 │    ├── medicos.py
 │    ├── enfermeros.py
 │    ├── cita.py
 │    ├── factura.py
 │
 └── main.py
🚀 Cómo Ejecutar el Proyecto

Clonar el repositorio.

Asegurarse de tener Python 3.10 o superior.

Ejecutar:

python main.py
🔒 Validaciones Implementadas

No se pueden agendar citas sin paciente.

No se pueden agendar citas sin profesional.

No se pueden reprogramar citas inexistentes.

Conversión segura de fechas mediante datetime.strptime.

📈 Posibles Mejoras Futuras

Persistencia de datos en archivos o base de datos.

Validación de disponibilidad del profesional.

Historial médico del paciente.

Interfaz gráfica.

Manejo de múltiples sedes.

Sistema de autenticación.
