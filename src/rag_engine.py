import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load API Key
load_dotenv()

class HSEReporter:
    def __init__(self, sop_path):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("❌ SECURITY ALERT: API Key Groq belum disetting di file .env!")
        
        # Inisialisasi Client
        self.client = Groq(api_key=self.api_key)
        self.sop_content = self._load_text_data(sop_path)
        
        # Setup CSV
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(base_dir, '..', 'data', 'incident_log.csv')
        self._init_db()

    def _load_text_data(self, path):
        if not os.path.exists(path):
            return "General Safety Rules (SOP File Not Found)."
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _init_db(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Violation", "Severity", "Zone", "Shift"])

    def _save_incident(self, violation, severity, zone="Zone 1 (Main Gate)", shift="Morning (06-14)"):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_hour = datetime.now().hour
            
            # Auto-detect shift
            if 6 <= current_hour < 14: shift = 'Morning (06-14)'
            elif 14 <= current_hour < 22: shift = 'Afternoon (14-22)'
            else: shift = 'Night (22-06)'
            
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, violation, severity, zone, shift])
            
            # Print konfirmasi di terminal (Bukan return string)
            print(f"📝 [DATABASE] Saved: {violation} | {severity}")
            return True
        except Exception as e:
            print(f"❌ Gagal save CSV: {e}")
            return False

    def process_incident(self, violation_type):
        # 1. RETRIEVAL (Cek konteks untuk multiple violations)
        context = "Aturan Umum K3"
        if "Hardhat" in violation_type: context += ", Pasal Helm"
        if "Vest" in violation_type: context += ", Pasal Rompi"
        if "Mask" in violation_type: context += ", Pasal Masker"
        
        # 2. REASONING (Prompt Khusus Multi-Pelanggaran)
        prompt = f"""
        Analisis INSIDEN GABUNGAN ini:
        - Daftar Pelanggaran: {violation_type}
        - Konteks SOP: {self.sop_content}
        
        Tugas: 
        1. Jika ada >1 pelanggaran, otomatis naikkan SEVERITY jadi HIGH.
        2. Tentukan Analisis Singkat.
        
        Format: SEVERITY|ANALISIS
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Kamu adalah Senior HSE Officer yang tegas."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile", 
                temperature=0.1
            )
            raw_answer = response.choices[0].message.content
            
            # 3. PARSING
            if "|" in raw_answer:
                severity, analysis = raw_answer.split('|', 1)
                severity = severity.strip().upper()
                analysis = analysis.strip()
            else:
                severity = "HIGH" # Default High kalau pelanggaran banyak
                analysis = raw_answer

            # 4. ACTION
            self._save_incident(violation_type, severity)
            
            return f"[{severity}] {analysis}"
                
        except Exception as e:
            print(f"❌ GROQ API ERROR: {e}")
            return "AI Error"