"""
Homoglyph Converter — Streamlit Version
Deploy ke Streamlit Cloud: https://streamlit.io/cloud
"""

import streamlit as st

# ── Mapping ───────────────────────────────────────────────────────────────────

LATIN_TO_CYRILLIC = {
    'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
    'x': 'х', 'y': 'у', 'A': 'А', 'B': 'В', 'C': 'С',
    'E': 'Е', 'H': 'Н', 'I': 'І', 'K': 'К', 'M': 'М',
    'O': 'О', 'P': 'Р', 'T': 'Т', 'X': 'Х', 'Y': 'У',
}
CYRILLIC_TO_LATIN = {v: k for k, v in LATIN_TO_CYRILLIC.items()}

# ── Logika konversi ───────────────────────────────────────────────────────────

def latin_to_cyrillic(text):
    return ''.join(LATIN_TO_CYRILLIC.get(c, c) for c in text)

def cyrillic_to_latin(text):
    return ''.join(CYRILLIC_TO_LATIN.get(c, c) for c in text)

def detect_characters(text):
    if not text.strip():
        return ""
    rows = []
    for char in text:
        code = ord(char)
        is_cyrillic = 0x0400 <= code <= 0x04FF
        is_latin = (0x0041 <= code <= 0x005A) or (0x0061 <= code <= 0x007A)
        is_homoglyph = char in LATIN_TO_CYRILLIC or char in CYRILLIC_TO_LATIN
        script = "Cyrillic" if is_cyrillic else ("Latin" if is_latin else "Other")
        note = "⚠️ HOMOGLYPH" if is_homoglyph else ""
        rows.append({
            "Char": repr(char),
            "Unicode": f"U+{code:04X}",
            "Script": script,
            "Keterangan": note,
        })
    return rows

def compare_strings(a, b):
    hasil = {
        "String A": a,
        "String B": b,
        "Identik?": "✅ YA" if a == b else "❌ TIDAK — tampak sama, beda Unicode!",
        "Panjang A": len(a),
        "Panjang B": len(b),
    }
    diffs = []
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            diffs.append(f"Posisi {i}: '{ca}' (U+{ord(ca):04X}) vs '{cb}' (U+{ord(cb):04X})")
    return hasil, diffs

# ── UI Streamlit ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Homoglyph Converter",
    page_icon="🔡",
    layout="centered"
)

# Inject font Inter dari Google Fonts
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"], .stTextArea, .stTextInput, .stRadio,
.stDataFrame, .stCaption, h1, h2, h3, p, div, span, label, button {
    font-family: 'Inter', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🔡 Homoglyph Converter")
st.caption("Latin ↔ Cyrillic homoglyph — terlihat sama di layar, Unicode berbeda")

st.divider()

mode = st.radio(
    "Pilih mode:",
    ["Latin → Cyrillic", "Cyrillic → Latin", "Deteksi Karakter", "Bandingkan 2 Teks"],
    horizontal=True
)

st.divider()

# ── Mode: Latin → Cyrillic ──
if mode == "Latin → Cyrillic":
    teks = st.text_area("Input (Latin):", placeholder="Ketik teks Latin di sini...", height=120)
    if teks:
        hasil = latin_to_cyrillic(teks)
        st.text_area("Hasil (Cyrillic homoglyph):", value=hasil, height=120)
        st.caption(f"Identik dengan input? `{teks == hasil}` — seharusnya `False` jika ada konversi")
        st.code(hasil, language=None)

# ── Mode: Cyrillic → Latin ──
elif mode == "Cyrillic → Latin":
    teks = st.text_area("Input (Cyrillic):", placeholder="Paste teks Cyrillic homoglyph di sini...", height=120)
    if teks:
        hasil = cyrillic_to_latin(teks)
        st.text_area("Hasil (Latin):", value=hasil, height=120)
        st.code(hasil, language=None)

# ── Mode: Deteksi Karakter ──
elif mode == "Deteksi Karakter":
    teks = st.text_area("Input teks:", placeholder="Ketik atau paste teks untuk dianalisis...", height=120)
    if teks:
        rows = detect_characters(teks)
        if rows:
            st.markdown("#### Hasil deteksi:")
            st.dataframe(rows, use_container_width=True)
            homoglyphs = [r for r in rows if "HOMOGLYPH" in r["Keterangan"]]
            if homoglyphs:
                st.warning(f"⚠️ Ditemukan **{len(homoglyphs)}** karakter homoglyph!")
            else:
                st.success("✅ Tidak ada homoglyph terdeteksi.")

# ── Mode: Bandingkan 2 Teks ──
elif mode == "Bandingkan 2 Teks":
    col1, col2 = st.columns(2)
    with col1:
        teks_a = st.text_area("String A:", placeholder="Teks pertama...", height=120)
    with col2:
        teks_b = st.text_area("String B:", placeholder="Teks kedua...", height=120)

    if teks_a or teks_b:
        hasil, diffs = compare_strings(teks_a, teks_b)
        st.markdown("#### Hasil perbandingan:")
        for k, v in hasil.items():
            st.markdown(f"**{k}:** `{v}`")
        if diffs:
            st.markdown("#### Perbedaan karakter:")
            for d in diffs:
                st.code(d)
        elif teks_a == teks_b and teks_a:
            st.success("Kedua string benar-benar identik.")

st.divider()

# ── Tabel mapping ──
with st.expander("📋 Lihat semua mapping karakter"):
    mapping_data = [
        {"Latin": k, "Cyrillic (homoglyph)": v, "Unicode Cyrillic": f"U+{ord(v):04X}"}
        for k, v in LATIN_TO_CYRILLIC.items()
    ]
    st.dataframe(mapping_data, use_container_width=True)
