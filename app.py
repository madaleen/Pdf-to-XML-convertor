from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pdf_to_musicxml.converter import PREFERRED_EXTENSIONS
from pdf_to_musicxml.converter import convert_pdf_to_musicxml


st.set_page_config(page_title="PDF to MusicXML", page_icon="♪", layout="centered")


def detect_audiveris_jar() -> Path | None:
    env_path = os.environ.get("AUDIVERIS_JAR")
    if env_path:
        candidate = Path(env_path).expanduser()
        if candidate.exists():
            return candidate

    common_roots = [ROOT, Path.cwd(), Path.home(), Path.home() / "Downloads", Path.home() / "Desktop"]
    for root in common_roots:
        if not root.exists():
            continue

        for pattern in ("**/*audiveris*.jar", "**/*Audiveris*.jar"):
            for candidate in root.glob(pattern):
                if candidate.is_file():
                    return candidate.resolve()

    return None


st.markdown(
    """
    <style>
      .stApp {
          :root {
            --bg: #0b0f17;
            --surface: rgba(16, 22, 34, 0.92);
            --surface-2: rgba(22, 29, 45, 0.96);
            --border: rgba(255, 255, 255, 0.10);
            --border-strong: rgba(255, 255, 255, 0.16);
            --text: #f4f7fb;
            --muted: #a7b2c6;
            --accent: #6ea8ff;
            --accent-2: #f7c873;
          }

        background:
          radial-gradient(circle at top left, rgba(108, 163, 255, 0.18), transparent 30%),
              radial-gradient(circle at top left, rgba(110, 168, 255, 0.18), transparent 28%),
              radial-gradient(circle at top right, rgba(247, 200, 115, 0.12), transparent 26%),
              linear-gradient(180deg, #0b0f17 0%, #0e1420 42%, #131a29 100%);
            color: var(--text);
          }

          .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
      .hero {

          .stMarkdown, .stText, .stCaption, .stMetric, .stLabel, label, p, span, div {
            color: var(--text);
          }

          .stMarkdown p, .stMarkdown span, .stCaption {
            color: var(--muted);
        padding: 2.25rem 1.75rem 1.5rem;

        border-radius: 1.8rem;
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(15, 23, 42, 0.08);
            background:
              linear-gradient(180deg, rgba(18, 25, 39, 0.96), rgba(13, 18, 29, 0.96));
            border: 1px solid var(--border);
            box-shadow: 0 26px 70px rgba(0, 0, 0, 0.35);
        font-size: 0.78rem;

        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0.6;
        margin-bottom: 0.4rem;
            color: var(--accent-2);
      .hero h1 {
        margin: 0;

        font-size: 2.6rem;
        letter-spacing: -0.05em;
        line-height: 1.02;
      }
      .hero p {
            color: var(--text);
        margin-top: 0.75rem;

        max-width: 58ch;
        line-height: 1.6;
        opacity: 0.78;
      }
            color: var(--muted);
        display: grid;

        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.75rem;
        margin-top: 1rem;
      }
      .step {
        padding: 0.85rem 0.95rem;

        border-radius: 0.95rem;
        background: rgba(15, 23, 42, 0.04);
        border: 1px solid rgba(15, 23, 42, 0.06);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            color: var(--text);
        display: block;

        margin-bottom: 0.2rem;
      }
      .panel {
            color: var(--text);
        margin-top: 1rem;

        padding: 1.25rem 1.25rem 1.4rem;
        border-radius: 1.25rem;
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid rgba(15, 23, 42, 0.08);
            background: var(--surface);
            border: 1px solid var(--border-strong);
            box-shadow: 0 16px 44px rgba(0, 0, 0, 0.25);
        margin-top: 0.9rem;

        font-size: 0.93rem;
        opacity: 0.72;
      }
            color: var(--muted);
        margin-top: 1rem;

        padding: 1rem 1rem 0.25rem;
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.80);
        border: 1px solid rgba(15, 23, 42, 0.08);
            background: var(--surface-2);
            border: 1px solid var(--border);
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.22);
          }

          .stFileUploader,
          .stSelectbox,
          .stTextInput,
          .stButton,
          [data-testid="stFileUploaderDropzone"],
          [data-testid="stSelectbox"],
          [data-testid="stTextInput"] {
            color: var(--text);
          }

          [data-testid="stFileUploaderDropzone"],
          [data-testid="stSelectbox"] > div,
          [data-testid="stTextInput"] > div {
            background: rgba(255, 255, 255, 0.04) !important;
            border-color: var(--border) !important;
          }

          [data-baseweb="select"] > div,
          [data-baseweb="input"] > div,
          [data-baseweb="textarea"] > div {
            background-color: rgba(255, 255, 255, 0.04) !important;
            color: var(--text) !important;
            border-color: var(--border) !important;
          }

          input,
          textarea {
            color: var(--text) !important;
          }

          [data-testid="stFileUploader"] button,
          [data-testid="stButton"] button {
            background: linear-gradient(180deg, #2d6ee7, #2453b3) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 0.8rem !important;
            box-shadow: 0 10px 24px rgba(36, 83, 179, 0.35) !important;
          }

          [data-testid="stFileUploader"] button:hover,
          [data-testid="stButton"] button:hover {
            background: linear-gradient(180deg, #3579f1, #2a5cc0) !important;
            border-color: rgba(255,255,255,0.18) !important;
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Local score converter</div>
      <h1>PDF to MusicXML</h1>
      <p>Drop in a score PDF, pick the output format, and convert it locally. The app will try to find Audiveris automatically, or you can upload the jar once instead of pasting a path every time.</p>
      <div class="step-row">
        <div class="step"><strong>1. Upload</strong><span>Drop the score PDF into the page.</span></div>
        <div class="step"><strong>2. Convert</strong><span>Choose MusicXML or compressed MusicXML.</span></div>
        <div class="step"><strong>3. Download</strong><span>Save the exported file and open it in MuseScore.</span></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="panel">', unsafe_allow_html=True)

pdf_file = st.file_uploader(
    "Drop your PDF here",
    type=["pdf"],
    help="Drag and drop a score PDF or browse for one.",
)

st.caption("The app will try to find Audiveris automatically. If it cannot, the button will explain what is missing.")

convert_pressed = st.button("Convert PDF", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if convert_pressed:
    if pdf_file is None:
        st.error("Upload a PDF before converting.")
        st.stop()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        pdf_path = temp_path / pdf_file.name
        pdf_path.write_bytes(pdf_file.getbuffer())

        output_dir = temp_path / "out"

        jar_path = detect_audiveris_jar()

        if jar_path is None:
            st.error("Audiveris was not found. Install it or set the AUDIVERIS_JAR environment variable.")
            st.info("Convert will not start without Audiveris. The PDF alone is not enough.")
            st.stop()

        try:
            result = convert_pdf_to_musicxml(
                java_exe="java",
                jar_path=jar_path,
                input_pdf=pdf_path,
                output_dir=output_dir,
                preferred_extensions=PREFERRED_EXTENSIONS["Compressed MusicXML (.mxl)"],
            )
        except RuntimeError as error:
            st.error(str(error))
            st.stop()

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.success(f"Converted to {result.exported_file.name}")

        left, right = st.columns([1.3, 1])
        with left:
            st.markdown("**Ready to download**")
            st.caption("Output: compressed MusicXML (.mxl)")
            st.download_button(
                label="Download converted file",
                data=result.exported_file.read_bytes(),
                file_name=result.exported_file.name,
                mime="application/octet-stream",
                use_container_width=True,
            )
        with right:
            st.metric("Format", "Compressed MusicXML")
            st.metric("Output", result.exported_file.suffix.upper())

        if result.stdout:
            st.caption("Audiveris output")
            st.code(result.stdout)
        if result.stderr:
            st.caption("Audiveris warnings")
            st.code(result.stderr)

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="note">
      If Audiveris is already installed somewhere common, the app will try to find it automatically. You only need to upload the jar if auto-detect misses it.
    </div>
    """,
    unsafe_allow_html=True,
)
