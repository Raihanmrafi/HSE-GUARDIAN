import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="HSE Guardian Command Center",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ HSE Guardian: Intelligent Command Center")
st.markdown("### ⚡ Real-time Agentic AI Monitoring & Predictive Analytics")
st.divider()

# --- 2. FUNGSI LOAD DATA ---
def get_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', 'data', 'incident_log.csv')
    
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    return pd.read_csv(csv_path)

placeholder = st.empty()

# --- 3. LOOPING UTAMA ---
while True:
    df = get_data()
    
    # Generate ID unik berdasarkan waktu saat ini
    # Ini trik agar Streamlit tidak error "Duplicate Element ID"
    unique_id = str(time.time())

    with placeholder.container():
        if df.empty:
            st.warning("⚠️ Data log belum ditemukan. Jalankan 'seed_data.py' atau 'main.py' dulu!")
        else:
            # --- KPI CARDS ---
            total_incidents = len(df)
            dangerous_zone = df['Zone'].mode()[0] if not df.empty else "-"
            dangerous_shift = df['Shift'].mode()[0] if not df.empty else "-"
            high_risk_count = len(df[df['Severity']=='HIGH'])
            
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Total Insiden (30 Hari)", total_incidents, "LIVE")
            kpi2.metric("Pelanggaran Berat", high_risk_count, "Risk Alert")
            kpi3.metric("Zona Paling Rawan", dangerous_zone, "Attention", delta_color="inverse")
            kpi4.metric("Shift Paling Rawan", dangerous_shift)

            st.markdown("---")

            # --- GRAFIK CHART ---
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📍 Sebaran Lokasi Insiden")
                fig_zone = px.pie(df, names='Zone', title='Distribusi Pelanggaran per Area', hole=0.4, 
                                  color_discrete_sequence=px.colors.sequential.RdBu)
                # FIX ERROR DISINI: Tambahkan key unik
                st.plotly_chart(fig_zone, use_container_width=True, key=f"chart_zone_{unique_id}")

            with col2:
                st.subheader("📉 Tren Waktu (Shift Analysis)")
                shift_counts = df.groupby(['Shift', 'Severity']).size().reset_index(name='Counts')
                fig_shift = px.bar(shift_counts, x='Shift', y='Counts', color='Severity', 
                                   title='Frekuensi Insiden per Shift Kerja', barmode='group',
                                   color_discrete_map={'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'})
                # FIX ERROR DISINI: Tambahkan key unik
                st.plotly_chart(fig_shift, use_container_width=True, key=f"chart_shift_{unique_id}")

            # --- PREDICTIVE ANALYTICS ---
            st.divider()
            st.subheader("🤖 Agentic AI Predictive Insight")
            
            if not df.empty:
                risk_zone = df['Zone'].mode()[0]
                risk_violation = df[df['Zone'] == risk_zone]['Violation'].mode()[0]
                
                warning_msg = f"""
                #### ⚠️ EARLY WARNING SYSTEM DETECTED
                Berdasarkan analisis pola data historis:
                1.  **High Risk Area:** **{risk_zone}** teridentifikasi anomali tertinggi.
                2.  **Top Violation:** **{risk_violation}** mendominasi tren.
                3.  **Shift Alert:** Waspada pada **{dangerous_shift}**.
                
                **REKOMENDASI AGENTIC:**
                - 🚨 Kirim notifikasi prioritas ke Supervisor {risk_zone}.
                - 🔍 Lakukan inspeksi mendadak (Sidak) APD sebelum {dangerous_shift} dimulai.
                """
                st.error(warning_msg)

            # --- LOG DATA ---
            with st.expander("📄 Lihat Log Data Mentah (Live Audit Trail)"):
                st.dataframe(df.sort_values(by="Timestamp", ascending=False).head(5), use_container_width=True)

    # Refresh setiap 2 detik
    time.sleep(2)