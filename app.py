import os
from abc import ABC, abstractmethod
import streamlit as st
from PIL import Image
import google.generativeai as genai

# ==============================================================================
# 1. SISTEM BRAND MODULAR (Dapat Ditambah Langsung di Sini)
# ==============================================================================
class BaseBrand(ABC):
    @property
    @abstractmethod
    def brand_name(self) -> str:
        pass

    @property
    @abstractmethod
    def official_website(self) -> str:
        pass

    @abstractmethod
    def format_search_query(self, extracted_text: str, tool_type: str) -> str:
        pass


class SnapOn(BaseBrand):
    @property
    def brand_name(self) -> str:
        return "Snap-on"
    
    @property
    def official_website(self) -> str:
        return "shop.snapon.com"

    def format_search_query(self, extracted_text: str, tool_type: str) -> str:
        return f"site:{self.official_website} {tool_type} {extracted_text} part number"


class EgaMaster(BaseBrand):
    @property
    def brand_name(self) -> str:
        return "EGA Master"
    
    @property
    def official_website(self) -> str:
        return "egamaster.com"

    def format_search_query(self, extracted_text: str, tool_type: str) -> str:
        return f"site:{self.official_website} {tool_type} {extracted_text} specification"


class Tekiro(BaseBrand):
    @property
    def brand_name(self) -> str:
        return "Tekiro"
    
    @property
    def official_website(self) -> str:
        return "tekiro.com"

    def format_search_query(self, extracted_text: str, tool_type: str) -> str:
        return f"site:{self.official_website} {tool_type} {extracted_text} kode item"


# Pendaftar Brand (Tambahkan class baru ke sini jika ada brand baru)
BRAND_REGISTRY = {
    "Snap-on": SnapOn(),
    "EGA Master": EgaMaster(),
    "Tekiro": Tekiro(),
    "FACOM": None,
    "Stahlwille": None,
    "Lainnya / Unknown": None
}


# ==============================================================================
# 2. LOGIKA ANALISIS AI (Vision, OCR, & Cross-Checking)
# ==============================================================================
class ToolAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def analyze_tool(self, image, brand: str, user_specs: str, web_context: str = "") -> str:
        prompt = f"""
        Tugas: Identifikasi Part Number dari Aviation/Industrial tool pada gambar ini.
        Prioritas Utama: AKURASI > KECEPATAN. Jangan berikan Part Number fiktif.
        
        Informasi dari User:
        - Brand: {brand}
        - Spesifikasi Tambahan: {user_specs}
        
        Konteks Pencarian Web / Brand:
        {web_context}
        
        Lakukan langkah berikut:
        1. OCR: Baca semua teks, kode, ukuran, atau ukiran yang ada di fisik tool.
        2. Visual Recognition: Identifikasi tipe tool (misal: Torque Wrench, Ratchet, Pliers) dan fitur uniknya.
        3. Cross-check: Cocokkan ciri visual dan hasil OCR dengan format penomoran part brand tersebut.
        4. Confidence Score: Tentukan tingkat kepastian (0-100%). Berikan skor < 50% jika Part Number hanya perkiraan visual tanpa teks terpisah yang jelas.
        
        Format Output Jawaban:
        - **Estimated Part Number:** [Nomor Part / Tidak Yakin]
        - **Confidence Score:** [0-100%]
        - **Identified Tool Type:** [Tipe Tool]
        - **Evidence & Reasoning:** [Detail temuan OCR dan visual]
        - **Human Verification Needed:** [Ya/Tidak dan catat alasannya]
        """
        
        response = self.model.generate_content([prompt, image])
        return response.text


# ==============================================================================
# 3. INTERFACE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Aviation Tool Part Number Finder",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Aviation Tool Part Number Finder")
st.markdown("Sistem AI untuk mengidentifikasi *Part Number* alat penerbangan & industri berdasarkan foto dan spesifikasi.")

# Mengambil API Key dari Streamlit Secrets / Environment
api_key = os.getenv("GEMINI_API_KEY")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Input Gambar")
    input_method = st.radio("Metode Input Gambar:", ["Upload File", "Kamera"])
    
    image_file = None
    if input_method == "Upload File":
        image_file = st.file_uploader("Upload foto tool (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    else:
        image_file = st.camera_input("Ambil foto tool")

    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Foto Tool yang Dianalisis", use_container_width=True)

with col2:
    st.header("2. Informasi Tambahan")
    selected_brand = st.selectbox("Brand Tool:", list(BRAND_REGISTRY.keys()))
    tool_type = st.text_input("Tipe Tool (misal: Ratchet, Torque Wrench, Obeng):")
    size_info = st.text_input("Ukuran (misal: 1/4 inch drive, 10mm):")
    additional_desc = st.text_area("Deskripsi / Engraving Teks yang Terlihat:")

st.divider()

if st.button("Mulai Identifikasi Part Number", type="primary"):
    if not image_file:
        st.error("⚠️ Silakan upload atau ambil foto tool terlebih dahulu.")
    elif not api_key:
        st.error("⚠️ API Key tidak ditemukan. Pastikan 'GEMINI_API_KEY' sudah diset di Streamlit Secrets.")
    else:
        with st.spinner("AI sedang menganalisis gambar, melakukan OCR, dan mencocokkan data..."):
            analyzer = ToolAnalyzer(api_key=api_key)
            user_specs = f"Type: {tool_type}, Size: {size_info}, Notes: {additional_desc}"
            
            # Memformat query berdasarkan brand jika terdaftar
            brand_handler = BRAND_REGISTRY.get(selected_brand)
            web_context = ""
            if brand_handler:
                web_context = f"Website Resmi: {brand_handler.official_website}"
            
            # Jalankan Analisis
            result_text = analyzer.analyze_tool(
                image=img,
                brand=selected_brand,
                user_specs=user_specs,
                web_context=web_context
            )
            
            st.success("Analisis Selesai!")
            st.markdown("### 📋 Hasil Identifikasi Part Number")
            st.markdown(result_text)
