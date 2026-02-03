import cv2
import os
import time
from detector import HSEDetector
from rag_engine import HSEReporter

def main():
    # --- 1. SETUP PATHS ---
    # Mencari lokasi file model dan SOP secara otomatis
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '..', 'models', 'yolo_hse.pt')
    sop_path = os.path.join(base_dir, '..', 'data', 'documents', 'sop_k3.txt')

    print("🚀 MENYIAPKAN HSE GUARDIAN SYSTEM...")
    
    # --- 2. INISIALISASI SISTEM ---
    # Cek Model YOLO (Mata)
    if not os.path.exists(model_path):
        print(f"❌ Error: Model vision tidak ditemukan di {model_path}")
        print("Pastikan file 'best.pt' sudah direname jadi 'yolo_hse.pt' dan ditaruh di folder models/")
        return
    
    try:
        detector = HSEDetector(model_path, conf_threshold=0.5)
        print("✅ Vision System (YOLO) Siap!")
    except Exception as e:
        print(f"❌ Gagal memuat YOLO: {e}")
        return

    # Cek Agent AI (Otak)
    agent = None
    try:
        agent = HSEReporter(sop_path)
        print("✅ Agentic AI (RAG) Siap! Terhubung ke Groq Cloud.")
    except Exception as e:
        print(f"⚠️ PERINGATAN: Agent AI gagal dimuat ({e}).")
        print("Sistem akan berjalan dalam mode 'CCTV Only' (Tanpa Log Otomatis).")
        print("👉 Cek apakah .env sudah ada isi GROQ_API_KEY?")

    # --- 3. BUKA KAMERA ---
    cap = cv2.VideoCapture(0) # Ganti angka 0 jadi 1 kalau pakai webcam eksternal
    cap.set(3, 1280) # Lebar
    cap.set(4, 720)  # Tinggi

    # Variabel Kontrol (Cooldown)
    last_report_time = 0
    report_cooldown = 8  # Jeda 8 detik antar laporan (biar gak spam)
    
    # Status Display di Layar
    current_status = "SYSTEM ACTIVE - MONITORING"
    status_color = (0, 255, 0) # Hijau
    ai_narrative = ""

    print("\n🎥 KAMERA AKTIF! Tekan 'Q' di jendela kamera untuk keluar.")
    print("---------------------------------------------------------")

    while True:
        success, frame = cap.read()
        if not success:
            break

        # A. DETEKSI VISUAL (YOLO)
        processed_frame, violations = detector.detect(frame)

        # B. LOGIKA AGENTIC (Jika ada pelanggaran)
        if violations:
            violation_type = ", ".join(violations) # Ambil pelanggaran secara lengkap
            
            # Cek apakah Cooldown sudah selesai?
            if time.time() - last_report_time > report_cooldown:
                print(f"⚡ PELANGGARAN KOMBO TERDETEKSI: {violation_type}")
                
                if agent:
                    # Tampilkan status "AI Sedang Berpikir..."
                    current_status = f"DETECTED: {violation_type} | AI ANALYZING..."
                    status_color = (0, 165, 255) # Oranye
                    
                    # --- ACTION: AI MIKIR & TULIS LAPORAN ---
                    print("🤖 Agent AI sedang menganalisis SOP & mencatat log...")
                    ai_narrative = agent.process_incident(violation_type)
                    print(f"✅ Log Tersimpan: {ai_narrative[:50]}...")
                    
                    # Update status layar jadi Merah (Alert)
                    current_status = f"ALERT: {violation_type} (LOGGED)"
                    status_color = (0, 0, 255) # Merah
                    
                    last_report_time = time.time()
            else:
                # Selama masa cooldown, pertahankan status merah
                if time.time() - last_report_time < 3:
                    pass 

        else:
            # Jika aman, reset status setelah 5 detik tenang
            if time.time() - last_report_time > 5:
                current_status = "ZONE SAFE - NO VIOLATIONS"
                status_color = (0, 255, 0) # Hijau
                ai_narrative = ""

        # C. GUI overlay (Tampilan Layar Keren)
        # Bikin kotak hitam semi-transparan di bawah untuk teks
        h, w, _ = processed_frame.shape
        overlay = processed_frame.copy()
        cv2.rectangle(overlay, (0, h-80), (w, h), (0, 0, 0), -1)
        alpha = 0.6 # Transparansi
        cv2.addWeighted(overlay, alpha, processed_frame, 1 - alpha, 0, processed_frame)

        # Tulis Status Utama
        cv2.putText(processed_frame, current_status, (20, h-45), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Tulis Narasi AI (Kecil di bawahnya)
        if ai_narrative:
            cv2.putText(processed_frame, f"AI Insight: {ai_narrative[:90]}...", (20, h-15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Tampilkan
        cv2.imshow("HSE Guardian - Integrated System", processed_frame)

        # Keluar pakai Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()