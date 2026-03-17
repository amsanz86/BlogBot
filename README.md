# AUTO VIRAL BLOG ENGINE 🚀

Sistema autónomo de generación de contenido viral con IA y frontend premium integrado.

## 📁 Estructura del Proyecto
- `agents/`: Agentes inteligentes (Tendencias, Escritor, Imágenes, Publicador).
- `web/`: Tu Blog Real (HTML/CSS/JS). Abre `index.html` para verlo.
- `main.py`: El corazón del sistema.
- `.env`: Configuración de tus llaves API.

---

## 🚀 Guía de Ejecución Paso a Paso

### 1. Configuración de API Keys
Abre el archivo `.env` en tu editor y completa los datos:
- **OPENAI_API_KEY**: Obtén tu llave en [platform.openai.com](https://platform.openai.com/api-keys). Si OpenAI no está disponible en tu región, el sistema cambiará automáticamente a Gemini.
- **GEMINI_API_KEY**: Obtén tu llave GRATIS en [aistudio.google.com](https://aistudio.google.com/). Es altamente recomendado configurarla.
- **TELEGRAM_BOT_TOKEN**: Crea tu bot en [@BotFather](https://t.me/botfather).
- **TELEGRAM_CHAT_ID**: Obtén tu ID con [@userinfobot](https://t.me/userinfobot).
*(Nota: Ya no necesitas API key de Reddit, la extracción de temas virales se hace automáticamente de forma gratuita sin necesidad de registrar app en Reddit).*

### 2. Ejecución del Motor
Abre una terminal en la carpeta del proyecto y ejecuta:
```powershell
python main.py
```
El sistema hará lo siguiente:
1. Buscará una tendencia viral.
2. Escribirá el artículo con GPT-4o-mini (Costo: ~$0.001).
3. Creará una imagen con Pollinations.ai (**GRATIS**).
4. Actualizará tu blog en la carpeta `web/` automáticamente.

### 3. Ver tu Blog
Simplemente entra en la carpeta `web/` y abre `index.html` en Chrome o Edge. ¡Verás el nuevo contenido aparecer solo!

---

## 🛠️ Preguntas Frecuentes

**¿Dónde se guardan los artículos?**
Se guardan en `web/data/posts.json`. Son archivos locales que puedes subir a internet.

**¿Cómo lo subo a Internet gratis?**
1. Sube tu carpeta a un repositorio de **GitHub**.
2. Ve a Settings -> Pages y activa la rama `main`.
3. Tu blog estará vivo en `https://tu-usuario.github.io`.

**¿Cunto cuesta mantenerlo?**
Gracias a nuestras optimizaciones, con solo **$5 USD** en OpenAI tienes para publicar **miles de artículos**. Las imágenes son ilimitadas y gratuitas.
