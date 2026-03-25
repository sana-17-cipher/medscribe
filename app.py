from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
from pdf_exporter import generate_pdf
from database import init_db, save_record, get_all_records, get_record_by_id, search_records, delete_record
from nlp_extractor import extract_medical_info, detect_status
from speech_handler import transcribe_audio, allowed_file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "medscribe2024")
CORS(app)

init_db()

# ── PAGE ROUTES ──────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/history")
def history():
    records = get_all_records()
    return render_template("history.html", records=records)

@app.route("/record/<int:record_id>")
def view_record(record_id):
    record = get_record_by_id(record_id)
    if not record:
        return "Record not found", 404
    record["structured_report"] = json.loads(record["structured_report"])
    return render_template("view_record.html", record=record)

# ── API ROUTES ───────────────────────────────────────

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json()
    transcript = data.get("transcript", "").strip()
    doc_type   = data.get("doc_type", "consultation")
    patient_name = data.get("patient_name", "").strip()

    if not transcript:
        return jsonify({"success": False, "error": "Transcript is empty"}), 400

    result = extract_medical_info(transcript, doc_type, patient_name)

    if not result["success"]:
        return jsonify(result), 500

    report = result["data"]
    status = detect_status(report)

    record_id = save_record(
        patient_name=patient_name or report.get("Patient", "Unknown"),
        doc_type=doc_type,
        transcript=transcript,
        structured_report=json.dumps(report),
        status=status
    )

    return jsonify({
        "success": True,
        "record_id": record_id,
        "report": report,
        "status": status
    })

@app.route("/api/search", methods=["GET"])
def api_search():
    records = search_records(
        patient_name=request.args.get("patient_name", ""),
        keyword=request.args.get("keyword", ""),
        doc_type=request.args.get("doc_type", "")
    )
    return jsonify({"success": True, "records": records})

@app.route("/api/record/<int:record_id>", methods=["DELETE"])
def api_delete(record_id):
    delete_record(record_id)
    return jsonify({"success": True})

@app.route("/api/export-pdf", methods=["POST"])
def api_export_pdf():
    data = request.get_json()
    
    patient_name = data.get("patient_name", "Patient")
    doc_type     = data.get("doc_type", "consultation")
    report_data  = data.get("report", {})
    transcript   = data.get("transcript", "")

    try:
        pdf_bytes = generate_pdf(patient_name, doc_type, report_data, transcript)
        
        filename = f"medscribe_{patient_name.replace(' ', '_')}_{doc_type}.pdf"
        
        from flask import Response
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    if "audio" not in request.files:
        return jsonify({"success": False, "error": "No audio file"}), 400
    
    audio_file = request.files["audio"]
    
    if not allowed_file(audio_file.filename):
        return jsonify({"success": False, "error": "Unsupported format. Use mp3, wav, m4a"}), 400
    
    result = transcribe_audio(audio_file)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)