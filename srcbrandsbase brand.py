from abc import ABC, abstractmethod

# =========================================
# 1. BLUEPRINT DASAR (Base Class)
# =========================================
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


# =========================================
# 2. IMPLEMENTASI MASING-MASING BRAND
# =========================================
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


# =========================================
# 3. REGISTRY (Pendaftar Otomatis)
# =========================================
# Tambahkan class brand ke dalam dictionary ini agar otomatis terbaca oleh Streamlit
BRAND_REGISTRY = {
    "Snap-on": SnapOn(),
    "EGA Master": EgaMaster(),
    "Tekiro": Tekiro(),
    "FACOM": None,       # Belum diimplementasikan
    "Stahlwille": None,  # Belum diimplementasikan
    "Unknown / Other": None
}

def get_brand_handler(brand_name: str) -> BaseBrand:
    """Fungsi untuk memanggil konfigurasi brand berdasarkan pilihan user."""
    return BRAND_REGISTRY.get(brand_name)
