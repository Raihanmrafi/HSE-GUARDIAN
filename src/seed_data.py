import pandas as pd
import random
from datetime import datetime, timedelta
import os

# --- KONFIGURASI DATA MODELING ---
# Ini adalah representasi entitas dunia nyata ke dalam kode
ZONES = ['Zone 1 (Main Gate)', 'Zone 2 (Storage Tank)', 'Zone 3 (Pipeline)', 'Zone 4 (Office)']
VIOLATIONS = ['NO-Hardhat', 'NO-Safety Vest', 'NO-Mask', 'NO-Gloves']
SEVERITY_LEVELS = ['LOW', 'MEDIUM', 'HIGH']

def generate_fake_data(num_rows=200):
    print(f"🌱 Sedang menanam {num_rows} data dummy untuk simulasi Predictive Analytics...")
    
    data = []
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30) # Data 30 hari terakhir

    for _ in range(num_rows):
        # 1. Random Waktu (Dalam 30 hari terakhir)
        random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
        timestamp = start_time + timedelta(seconds=random_seconds)
        
        # 2. Tentukan Shift berdasarkan Jam (Data Logic)
        hour = timestamp.hour
        if 6 <= hour < 14:
            shift = 'Morning (06-14)'
        elif 14 <= hour < 22:
            shift = 'Afternoon (14-22)'
        else:
            shift = 'Night (22-06)'

        # 3. REKAYASA POLA (The Secret Sauce)
        # Biar dashboard nanti bilang "Zone 2 Bahaya!", kita perbanyak pelanggaran di situ.
        # Logika: Jika Shift Malam, 60% kemungkinan insiden terjadi di Zone 2.
        if shift == 'Night (22-06)' and random.random() < 0.6:
            zone = 'Zone 2 (Storage Tank)'
            violation = 'NO-Hardhat' # Orang sering lepas helm pas malam (contoh)
            severity = 'HIGH'        # Risiko tinggi
        else:
            # Data acak biasa (Noise)
            zone = random.choice(ZONES)
            violation = random.choice(VIOLATIONS)
            # Bobot severity: Lebih banyak LOW daripada HIGH (realistis)
            severity = random.choices(SEVERITY_LEVELS, weights=[50, 30, 20])[0]

        # Masukkan ke list
        data.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), violation, severity, zone, shift])

    # 4. Simpan ke CSV (Database Flat-file)
    # Naik satu folder dari 'src' ke root, lalu masuk 'data'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, '..', 'data', 'incident_log.csv')
    
    # Pastikan folder data ada
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    df = pd.DataFrame(data, columns=["Timestamp", "Violation", "Severity", "Zone", "Shift"])
    
    # Sort berdasarkan waktu biar rapi
    df = df.sort_values(by="Timestamp", ascending=True)
    
    df.to_csv(save_path, index=False)
    print(f"✅ Sukses! Database masa lalu berhasil dibuat di:\n   👉 {save_path}")
    print(f"📊 Total Data: {len(df)} baris.")

if __name__ == "__main__":
    generate_fake_data()