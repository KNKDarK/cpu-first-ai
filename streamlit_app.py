import sys
import json
import time
from pathlib import Path
import subprocess

import streamlit as st

from storage import DB_FILE, LOCK_FILE, fetch_recent, persist_output

st.set_page_config(
    page_title="Image Text Extractor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp { background: #0a0a0f; }
.block-container { padding-top: 1.5rem; }

.card {
    background: #13131a;
    border: 1px solid #1e1e2a;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.stFileUploader {
    border: 2px dashed #2a2a3a;
    border-radius: 16px;
    padding: 0.5rem;
}
.stFileUploader:hover { border-color: #a855f7; }

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.3);
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}
.status-idle {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
}
.status-busy {
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 1; }
}

.metric-card {
    text-align: center;
    padding: 1rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #fff;
}
.metric-label {
    font-size: 0.75rem;
    color: #6b6b80;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.25rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

hr { border-color: #1e1e2a; margin: 1.5rem 0; }
.stCodeBlock { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# Header
col_logo, col_status = st.columns([6, 2])
is_busy = LOCK_FILE.exists()
badge_cls = "status-busy" if is_busy else "status-idle"
badge_txt = "● Processing..." if is_busy else "● Idle / Ready"
with col_logo:
    st.markdown("""<div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.25rem;">
        <div style="background:linear-gradient(135deg,#a855f7,#3b82f6);width:10px;height:36px;border-radius:6px;"></div>
        <div>
            <h1 style="margin:0;font-size:1.6rem;font-weight:700;color:#fff;">Image Text Extractor</h1>
            <p style="margin:0;color:#6b6b80;font-size:0.85rem;">OCR + AI-powered text refinement</p>
        </div>
    </div>""", unsafe_allow_html=True)
with col_status:
    st.markdown(f"<div style='text-align:right;padding-top:0.5rem;'><span class='status {badge_cls}'>{badge_txt}</span></div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Main layout
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("<h3 style='margin-bottom:0.75rem;'>📷 Upload Image</h3>", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="uploader",
    )

    if uploaded is not None:
        st.image(uploaded, width="stretch")

with right:
    st.markdown("<h3 style='margin-bottom:0.75rem;'>📝 Extracted Text</h3>", unsafe_allow_html=True)

    result = st.session_state.get("result")

    if uploaded is not None and not is_busy and st.button("🔍 Extract Text", width="stretch", type="primary"):
        app_dir = Path(__file__).resolve().parent
        temp_path = app_dir / "temp_uploaded_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())

        # Step 1: OCR — use absolute path so it works on Streamlit Cloud
        with st.spinner("Step 1/2: Running OCR on image..."):
            proc = subprocess.run(
                [sys.executable, str(app_dir / "ingestion.py"), str(temp_path)],
                capture_output=True, text=True,
                cwd=str(app_dir),
            )
            raw_path = Path("/tmp/input.txt")
            raw_ocr_path = Path("/tmp/input_raw.txt")
            corrected_text = raw_path.read_text(encoding="utf-8").strip() if raw_path.exists() else None
            raw_ocr_text = (
                raw_ocr_path.read_text(encoding="utf-8").strip()
                if raw_ocr_path.exists()
                else corrected_text
            )

        if not corrected_text or corrected_text == "FAILED":
            # Surface the actual subprocess error so we can debug on cloud
            ocr_error_detail = ""
            if proc.returncode != 0 and proc.stderr.strip():
                ocr_error_detail = f"\n\nDebug info: {proc.stderr.strip()[:400]}"
            elif proc.stderr.strip():
                ocr_error_detail = f"\n\nDebug info: {proc.stderr.strip()[:400]}"
            st.session_state["result"] = {
                "raw": None,
                "corrected": None,
                "refined": None,
                "record_id": None,
                "error": f"OCR could not extract text from this image. Try a clearer image.{ocr_error_detail}",
            }
            st.rerun()

        # Step 2: LLM post-process — use absolute path so it works on Streamlit Cloud
        with st.spinner("Step 2/2: Post-processing with AI..."):
            transform_proc = subprocess.run(
                [sys.executable, str(app_dir / "transformation.py")],
                capture_output=True, text=True,
                cwd=str(app_dir),
            )
            out_path = Path("/tmp/output.json")
            refined_text = None
            record_id = None
            if out_path.exists():
                try:
                    data = json.loads(out_path.read_text(encoding="utf-8"))
                    if data.get("status") != "error":
                        refined_text = data.get("cleaned_text", "")
                        record_id = persist_output(
                            source_image=uploaded.name,
                            raw_text=raw_ocr_text,
                            corrected_text=corrected_text,
                            output_path=out_path,
                            db_path=DB_FILE,
                        )
                except Exception:
                    pass

        temp_path.unlink(missing_ok=True)
        for p in [raw_path, raw_ocr_path, out_path]:
            p.unlink(missing_ok=True)

        error = None
        if transform_proc.returncode != 0:
            error = "AI refinement failed. Showing corrected OCR instead."

        st.session_state["result"] = {
            "raw": raw_ocr_text,
            "corrected": corrected_text,
            "refined": refined_text,
            "record_id": record_id,
            "error": error,
        }
        st.rerun()

    if result is None:
        if uploaded is None:
            st.markdown("""<div class="card" style="text-align:center;padding:3rem 1rem;color:#6b6b80;">
                <div style="font-size:3rem;margin-bottom:1rem;">🖼️</div>
                <p style="margin:0;">Upload an image to extract text</p>
                <p style="font-size:0.8rem;margin-top:0.5rem;">Supports JPG, JPEG, PNG</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="card" style="text-align:center;padding:2rem 1rem;color:#6b6b80;">
                <p style="margin:0;">Click <strong>"Extract Text"</strong> to start</p>
            </div>""", unsafe_allow_html=True)

    elif result.get("error"):
        if result.get("raw") or result.get("corrected"):
            st.warning(result["error"])
            st.code(result.get("corrected") or result.get("raw"), language="text")
        else:
            st.error(result["error"])
        if st.button("🔄 Try Again", width="stretch"):
            st.session_state.pop("result", None)
            st.rerun()

    else:
        raw = result.get("raw", "")
        corrected = result.get("corrected") or raw
        refined = result.get("refined")

        tab_default, tab_corrected, tab_raw = st.tabs(
            ["✨ Intelligent Extraction", "✅ Corrected OCR", "📄 Raw OCR"]
        )

        with tab_default:
            if refined:
                st.code(refined, language="text")
                w = len(refined.split())
                c = len(refined)
                l = len([x for x in refined.split("\n") if x.strip()])
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""<div class="card metric-card"><div class="metric-value">{w}</div><div class="metric-label">Words</div></div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""<div class="card metric-card"><div class="metric-value">{c}</div><div class="metric-label">Characters</div></div>""", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""<div class="card metric-card"><div class="metric-value">{l}</div><div class="metric-label">Lines</div></div>""", unsafe_allow_html=True)
            else:
                st.info("AI refinement unavailable — showing corrected OCR instead.")
                st.code(corrected, language="text")

        with tab_corrected:
            st.code(corrected, language="text")

        with tab_raw:
            st.code(raw, language="text")

        if result.get("record_id"):
            st.caption(f"Saved to SQLite as extraction #{result['record_id']}.")

        if st.button("🔄 Extract Another", width="stretch"):
            st.session_state.pop("result", None)
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-bottom:0.75rem;'>Recent Extractions</h3>", unsafe_allow_html=True)

history = fetch_recent(limit=5, db_path=DB_FILE)
if not history:
    st.caption("No stored extractions yet.")
else:
    for item in history:
        with st.expander(f"#{item.id} · {item.source_image or 'Uploaded image'} · {item.created_at}"):
            st.code(item.cleaned_text, language="text")
