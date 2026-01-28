# Observabilidad Multi-Agente con LangSmith y Langfuse

## Objetivo

Configurar un entorno de Python reproducible para ejecutar flujos de trabajo multi-agente con observabilidad.
Instalar dependencias, configurar variables de entorno y ejecutar dos scripts de demostración:

* `multi_agent_langsmith.py` – Trazas con LangSmith
* `multi_agent_langfuse.py` – Trazas con Langfuse

Ambas demos muestran el enrutamiento de consultas entre agentes de RRHH y Tecnología con trazabilidad completa.

## Pasos

1. **Abrir una terminal** en este directorio y verificar los archivos:

   ```bash
   ls
   ```

2. **Crear y activar un entorno virtual**:

   * **venv** (Linux/macOS/Windows PowerShell):

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate    # Unix/macOS
     .\.venv\Scripts\activate     # Windows PowerShell
     ```
   * **conda**:

     ```bash
     conda create -n multi-agent python=3.10
     conda activate multi-agent
     ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear un archivo `.env`** con las siguientes variables:

   ```bash
   OPENAI_API_KEY=XXX

   # LangSmith
   LANGCHAIN_API_KEY=XXX
   LANGCHAIN_PROJECT=sh-multi-agent-demo
   LANGCHAIN_TRACING=true

   # Langfuse
   LANGFUSE_SECRET_KEY=XXX
   LANGFUSE_PUBLIC_KEY=XXX
   LANGFUSE_BASE_URL=https://cloud.langfuse.com
   ```

5. **Ejecutar las demos**:

   * **LangSmith**:

     ```bash
     python multi_agent_langsmith.py
     ```
   * **Langfuse**:

     ```bash
     python multi_agent_langfuse.py
     ```

6. **CLI interactiva**:

   * Escribí consultas como:

     ```
     ¿Cuántos días de vacaciones tengo?
     ¿Por qué no se conecta mi VPN?
     ```
   * Escribí `exit` para salir.

## Solución de problemas

* **Variables de entorno faltantes**: asegurate de que todas las claves estén correctamente definidas en el archivo `.env`.
* **Errores de API key**: verificá tus claves de OpenAI, LangSmith y Langfuse.
* **Problemas con paquetes**: actualizá pip y reinstalá las dependencias:

  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
