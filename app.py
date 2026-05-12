import os
import base64
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_IMAGES = 15
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def encode_image(file_bytes, media_type):
    return base64.b64encode(file_bytes).decode("utf-8"), media_type


def build_prompt(params):
    ocasion = params.get("ocasion", "no especificada")
    estilo = params.get("estilo", "no especificado")
    clima = params.get("clima", "no especificado")
    colores_evitar = params.get("colores_evitar", "ninguno")
    notas = params.get("notas", "")

    prompt = f"""Eres un estilista experto. El usuario te ha enviado fotos de prendas de ropa de su armario.

Tu tarea es armar UN outfit completo y cohesivo usando algunas de esas prendas (no tienes que usar todas).

PARÁMETROS DEL USUARIO:
- Ocasión: {ocasion}
- Estilo buscado: {estilo}
- Clima / temperatura: {clima}
- Colores a evitar: {colores_evitar}
- Notas adicionales: {notas if notas else "Ninguna"}

INSTRUCCIONES:
1. Analiza todas las prendas recibidas (las imágenes pueden mostrar varias prendas).
2. Selecciona las que mejor combinen según los parámetros dados.
3. Arma un outfit completo y describe exactamente qué prendas usas (siendo específico: color, tipo de prenda, cualquier detalle visible).
4. Explica por qué esa combinación funciona para la ocasión y el estilo pedido.
5. Da un consejo de cómo lucir mejor el outfit (accesorios sugeridos, calzado ideal, etc.).
6. Si alguna prenda enviada NO encaja con los parámetros, menciona por qué la descartaste.

Responde  con una foto de un outfit completo que combine con las prendas analizadas y los parámetros dados. Si no puedes generar una foto, responde con una descripción detallada del outfit sugerido."""
    print("Prompt generado para OpenAI:")
    print(prompt)
    return prompt


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/outfit", methods=["POST"])
def generar_outfit():
    if "imagenes" not in request.files:
        return jsonify({"error": "No se enviaron imágenes"}), 400

    files = request.files.getlist("imagenes")
    valid_files = [f for f in files if f and allowed_file(f.filename)]

    if not valid_files:
        return jsonify({"error": "No se encontraron imágenes válidas (jpg, png, webp)"}), 400

    if len(valid_files) > MAX_IMAGES:
        return jsonify({"error": f"Máximo {MAX_IMAGES} imágenes permitidas"}), 400

    params = {
        "ocasion": request.form.get("ocasion", ""),
        "estilo": request.form.get("estilo", ""),
        "clima": request.form.get("clima", ""),
        "colores_evitar": request.form.get("colores_evitar", ""),
        "notas": request.form.get("notas", ""),
    }

    content = [{"type": "text", "text": build_prompt(params)}]

    for f in valid_files:
        file_bytes = f.read()
        ext = f.filename.rsplit(".", 1)[1].lower()
        media_type_map = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
            "gif": "image/gif",
        }
        media_type = media_type_map.get(ext, "image/jpeg")
        b64, mt = encode_image(file_bytes, media_type)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mt};base64,{b64}",
                "detail": "high"
            }
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
            max_tokens=1500,
        )
        resultado = response.choices[0].message.content
        return jsonify({"outfit": resultado, "prendas_analizadas": len(valid_files)})

    except Exception as e:
        return jsonify({"error": f"Error al consultar OpenAI: {str(e)}"}), 500


if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0', port=5000)
