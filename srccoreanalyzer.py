import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Optional

# Skema output terstruktur untuk AI (Pydantic)
class PartNumberResult(BaseModel):
    part_number: str
    confidence_score: int
    tool_type: str
    evidence_reasoning: str
    needs_human_verification: bool
    source_url: Optional[str]

class ToolAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Menggunakan model vision-language terkini
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def analyze_tool(self, image, brand: str, user_specs: str, web_search_results: str = "") -> dict:
        prompt = f"""
        Tugas: Identifikasi Part Number dari Aviation/Industrial tool pada gambar ini.
        Prioritas Utama: AKURASI > KECEPATAN. Jangan berikan Part Number fiktif. Jika tidak yakin, nyatakan butuh verifikasi manusia.
        
        Informasi dari User:
        - Brand: {brand}
        - Spesifikasi Tambahan: {user_specs}
        
        Data Pencarian Web (Referensi Katalog Resmi):
        {web_search_results}
        
        Lakukan langkah berikut dalam analisismu:
        1. OCR: Baca semua teks, ukuran, atau ukiran pada fisik tool.
        2. Visual Recognition: Identifikasi tipe tool (misal: Torque Wrench, Ratchet, Pliers).
        3. Cross-check: Cocokkan ciri visual dan OCR dengan data katalog web yang disediakan.
        4. Scoring: Berikan confidence score (0-100). Harus di bawah 50 jika hanya berdasarkan tebakan visual tanpa konfirmasi teks/web.
        
        Kembalikan hasil dalam format JSON yang mencakup: part_number, confidence_score, tool_type, evidence_reasoning, needs_human_verification, source_url.
        """
        
        # Eksekusi AI Vision
        response = self.model.generate_content([prompt, image])
        
        # Parsing JSON response dari AI (disederhanakan untuk contoh)
        try:
            return response.text # Dalam implementasi penuh, gunakan json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}