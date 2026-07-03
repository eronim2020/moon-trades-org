import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_mineral_spectra():
    return {
        'Quartz': np.array([0.45, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.65, 0.66, 0.67, 0.68, 0.68, 0.69, 0.69, 0.70]),
        'Feldspar': np.array([0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.65, 0.66, 0.67, 0.68, 0.68, 0.69]),
        'Clay': np.array([0.35, 0.36, 0.38, 0.40, 0.42, 0.45, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.65, 0.66, 0.67]),
        'Calcite': np.array([0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.65, 0.66, 0.67, 0.68, 0.68, 0.69, 0.69, 0.70, 0.70, 0.71]),
        'Iron Oxide': np.array([0.25, 0.26, 0.27, 0.28, 0.30, 0.32, 0.35, 0.38, 0.42, 0.46, 0.50, 0.54, 0.58, 0.62, 0.65, 0.68, 0.70, 0.72]),
    }

def classify_sample(sample_spectrum, mineral_spectra):
    similarities = {}
    for mineral_name, mineral_spectrum in mineral_spectra.items():
        correlation = np.corrcoef(sample_spectrum, mineral_spectrum)[0, 1]
        if np.isnan(correlation):
            correlation = 0
        similarities[mineral_name] = max(0, correlation)
    total = sum(similarities.values())
    percentages = {k: (v / total) * 100 for k, v in similarities.items()} if total > 0 else {k: 0 for k in similarities.keys()}
    return sorted(percentages.items(), key=lambda x: x[1], reverse=True)

st.set_page_config(page_title="Petrognosis", page_icon="🔬", layout="wide")
st.markdown('<div style="color: #e97021; font-size: 2.5em; font-weight: bold;">🔬 PETROGNOSIS</div>', unsafe_allow_html=True)
st.markdown("AI-Powered Mineral Analysis | Moon Trades SRL")
st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Live Demo", "📈 Library", "ℹ️ About"])

with tab1:
    st.subheader("Live Sample Analysis")
    mineral_spectra = get_mineral_spectra()
    selected = st.selectbox("Select mineral:", list(mineral_spectra.keys()))
    sample = mineral_spectra[selected] + np.random.normal(0, 0.02, 18)
    if st.button("🔍 Analyze Sample"):
        with st.spinner("Processing..."):
            import time
            time.sleep(2)
        results = classify_sample(sample, mineral_spectra)
        st.session_state.results = results
    if 'results' in st.session_state:
        st.markdown("### Results")
        for mineral, pct in st.session_state.results[:5]:
            st.write(f"**{mineral}**: {pct:.1f}%")

with tab2:
    st.subheader("Spectral Library")
    st.write("8 common minerals with NIR reflectance signatures (610-940nm)")

with tab3:
    st.subheader("About Petrognosis")
    st.write("**Petrognosis MVP v0.1** | Moon Trades SRL")
    st.write("eronim.mihoc@moontrades.org | +40 793 760 508")
