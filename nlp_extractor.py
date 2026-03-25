from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DOC_FIELDS = {
    "consultation": [
        "Patient", "Chief Complaint", "Symptoms", "Duration",
        "Allergies", "Diagnosis", "Prescription", "Follow-up", "Notes"
    ],
    "preop": [
        "Patient", "Age", "Diagnosis", "Planned Procedure",
        "Allergies", "Blood Group", "Pre-op Tests", "Consent", "Surgeon", "Notes"
    ],
    "intraop": [
        "Patient", "Surgeon", "Assistants", "Anesthetist",
        "Start Time", "End Time", "Anesthesia Type", "Procedure",
        "Blood Loss", "Complications", "Findings", "Notes"
    ],
    "postop": [
        "Patient", "Procedure Done", "Condition", "BP",
        "Pulse", "SpO2", "Pain Level", "Medications",
        "Diet Instructions", "Notes"
    ],
    "anesthesia": [
        "Patient", "Anesthetist", "Anesthesia Type", "Drugs Given",
        "Dosage", "Induction Time", "Patient Response", "Vitals", "Recovery Notes"
    ],
    "nursing": [
        "Patient", "Nurse", "Positioning", "Sterility Status",
        "Instrument Count", "Sponge Count", "Monitoring Notes", "Observations"
    ],
    "operative": [
        "Patient", "Surgeon", "Final Diagnosis", "Procedure Performed",
        "Surgical Findings", "Technique Used", "Complications",
        "Blood Loss", "Condition After Surgery", "Notes"
    ]
}

def extract_medical_info(transcript: str, doc_type: str, patient_name: str = "") -> dict:
    fields = DOC_FIELDS.get(doc_type, DOC_FIELDS["consultation"])

    prompt = f"""You are a medical documentation AI assistant.
A doctor has dictated the following clinical note. Extract and structure the information.

Document Type: {doc_type.upper()}
Patient Name (if known): {patient_name or 'Extract from transcript if mentioned'}
Dictation: "{transcript}"

Return ONLY a valid JSON object with these exact keys:
{json.dumps(fields, indent=2)}

Rules:
1. Extract values from the transcript. If a field is not mentioned, use "Not mentioned".
2. For Symptoms, include duration in brackets e.g. "Fever (3 days)".
3. For Condition or Status use exactly: "Stable", "Critical", or "Unknown".
4. For medications include dosage and frequency if mentioned.
5. Keep values concise and clinical.
6. Return ONLY the JSON. No explanation, no markdown backticks, no extra text."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return {"success": True, "data": result}
    except json.JSONDecodeError:
        return {"success": False, "error": "Could not parse AI response", "raw": raw}
    except Exception as e:
        return {"success": False, "error": str(e)}

def detect_status(report_data: dict) -> str:
    for key in ["Condition", "Status", "Condition After Surgery"]:
        val = report_data.get(key, "").lower()
        if "stable" in val:
            return "Stable"
        if "critical" in val:
            return "Critical"
    return "Unknown"