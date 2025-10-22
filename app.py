from flask import Flask, render_template, request
import whisper
import os
from werkzeug.utils import secure_filename

# Configuración inicial
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'opus'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cargar modelo Whisper (base)
print("🧠 Cargando modelo Whisper... puede tardar unos segundos.")
model = whisper.load_model("base")
print("✅ Modelo Whisper cargado correctamente.")

# Función para validar extensiones
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    transcriptions = []
    error = None

    if request.method == 'POST':
        if 'audiofile' not in request.files:
            error = "No se encontraron archivos."
        else:
            files = request.files.getlist('audiofile')
            if not files or files[0].filename == '':
                error = "No se seleccionaron archivos."
            else:
                for file in files:
                    filename = secure_filename(file.filename)
                    if not allowed_file(filename):
                        print(f"⚠️ Archivo no permitido: {filename}")
                        transcriptions.append((filename, "Formato no permitido."))
                        continue

                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    print(f"📁 Archivo guardado: {filepath}")

                    # Transcripción
                    try:
                        print(f"🎙️ Iniciando transcripción de: {filename}")
                        result = model.transcribe(filepath, language="es")
                        text = result.get("text", "").strip()

                        if text:
                            print(f"✅ Transcripción completada ({filename})")
                            print(f"📝 Texto: {text[:100]}{'...' if len(text) > 100 else ''}")
                            transcriptions.append((filename, text))
                        else:
                            print(f"⚠️ No se detectó texto en {filename}")
                            transcriptions.append((filename, "[Sin texto detectado]"))
                    except Exception as e:
                        error_msg = f"❌ Error transcribiendo {filename}: {e}"
                        print(error_msg)
                        transcriptions.append((filename, error_msg))

    return render_template('index.html', transcriptions=transcriptions, error=error)

# Iniciar servidor Flask
if __name__ == '__main__':
    app.run(debug=True)