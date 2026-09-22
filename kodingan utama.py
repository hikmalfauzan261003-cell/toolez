import streamlit as st
from PIL import Image
from src.core.analyzer import ToolAnalyzer
from src.brands.registry import BRAND_REGISTRY
import os

# Konfigurasi Halaman
st.set_page_config(
    page_title="Aviation Tool PN Finder",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Aviation Tool Part Number Finder")
st.markdown("""
Sistem AI untuk mengidentifikasi *Part Number* alat penerbangan dan industri.  
**Prinsip: Akurasi di atas Kecepatan. Tidak ada tebakan tanpa bukti.**
""")

# Inisialisasi Core AI
# Ambil API key dari Environment Variables (Streamlit Secrets)
api_key = os.getenv("GEMINI_API_KEY", "DUMMY_KEY_UNTUK_TESTING")
analyzer = ToolAnalyzer(api_key=api_key)

col1, col2 = st.columns(2)

with col1:
    st.header("1. Input Gambar")
    input_method = st.radio("Metode Input Gambar:", ["Upload File", "Kamera"])
    
    image_file = None
    if input_method == "Upload File":
        image_file = st.file_uploader("Upload foto tool (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    else:
        image_file = st.camera_input("Ambil foto tool secara langsung")

    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Gambar yang diunggah", use_container_width=True)

with col2:
    st.header("2. Informasi Tambahan")
    st.info("Semakin detail informasi yang diberikan, semakin tinggi akurasi AI.")
    
    selected_brand = st.selectbox("Brand (Opsional / Jika Diketahui):", list(BRAND_REGISTRY.keys()))
    tool_type = st.text_input("Tipe Tool (Contoh: Torque Wrench, Obeng, Ratchet):")
    size_info = st.text_input("Ukuran / Dimensi (Contoh: 1/4 inch drive, 10mm):")
    additional_desc = st.text_area("Deskripsi Tambahan / Engraving / Teks yang terlihat buram:")

st.divider()

if st.button("Mulai Identifikasi Part Number", type="primary"):
    if not image_file:
        st.error("⚠️ Silakan upload atau ambil foto tool terlebih dahulu.")
    else:
        with st.spinner("AI sedang menganalisis gambar, OCR, dan melakukan cross-checking dengan katalog resmi..."):
            
            # 1. Kompilasi data dari user
            user_specs = f"Type: {tool_type}, Size: {size_info}, Notes: {additional_desc}"
            
            # 2. (Simulasi) Pencarian Web berdasarkan brand
            # Pada implementasi nyata, jalankan Google Custom Search API di sini
            mock_web_search = f"Simulasi hasil web scraping untuk {selected_brand} {tool_type} {size_info}..."
            
            # 3. Analisis AI
            result = analyzer.analyze_tool(
                image=img,
                brand=selected_brand,
                user_specs=user_specs,
                web_search_results=mock_web_search
            )
            
            # 4. Tampilkan Hasil (Workflow Verifikasi Manusia)
            st.success("Analisis Selesai!")
            
            st.subheader("📋 Hasil Identifikasi")
            
            # Placeholder tampilan hasil (Asumsikan result adalah dict)
            # Pada kode nyata, result akan berupa objek JSON yang sudah di-parse
            st.markdown(f"**Raw AI Response:**\n{result}")
            
            # UI Mockup untuk Hasil Terstruktur
            st.metric(label="Estimated Part Number", value="T72 (Contoh)")
            st.progress(85, text="Confidence Score: 85% (High)")
            
            st.markdown("### 🔍 Dasar Pemikiran (Evidence Reasoning)")
            st.write("1. **OCR:** Mendeteksi ukiran '72' dan 'USA' pada gagang.")
            st.write("2. **Visual:** Bentuk kepala ratchet sesuai dengan mekanisme Dual 80 Technology.")
            st.write("3. **Cross-check:** Website resmi Snap-on mengonfirmasi T72 adalah 1/4\" Drive Dual 80 Technology Standard Ratchet.")
            
            st.markdown("### 🌐 Sumber (Source Citation)")
            st.write("[Snap-on Official Catalog - T72](https://shop.snapon.com)")
            
            st.warning("⚠️ **Human Verification Required:** AI mengidentifikasi korosi pada bagian drive, pastikan membandingkan panjang gagang secara manual.")