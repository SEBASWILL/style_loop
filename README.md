# 👗 Outfit AI

Aplicación web que analiza fotos de tu ropa usando **GPT-4o Vision** y arma un outfit personalizado según tus parámetros.

## Instalación

1. **Clona o descarga** este proyecto

2. **Instala dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura tu API key:**
   ```bash
   cp .env.example .env
   # Edita .env y pon tu OPENAI_API_KEY real
   ```

4. **Corre el servidor:**
   ```bash
   python app.py
   ```

5. **Abre en el navegador:** `http://localhost:5000`

## Uso

1. **Sube fotos** de tus prendas (máx. 15 imágenes)
2. **Define parámetros:** ocasión, estilo, clima, colores a evitar
3. Haz clic en **"Armar mi outfit"** y espera ~10-15 segundos
4. La IA analiza todas tus prendas y sugiere la mejor combinación

## Estructura

```
outfit-ai/
├── app.py              ← Backend Flask
├── requirements.txt    ← Dependencias
├── .env.example        ← Template de configuración
└── templates/
    └── index.html      ← Frontend completo
```

## Notas
- Requiere una API key de OpenAI con acceso a `gpt-4o`
- Cada consulta usa tokens de la API (costo aproximado: $0.02–0.10 por consulta según cantidad de imágenes)
- Las imágenes **no se guardan** en el servidor; se procesan en memoria y se envían directamente a la API
