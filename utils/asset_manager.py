# utils/asset_manager.py
import os
import streamlit as st

# Fungsi untuk memastikan path absolut ke asset
def get_asset_path(filename):
    current_dir = os.path.dirname(__file__)  # Lokasi file Python ini
    asset_dir = os.path.join(current_dir, "../asset")  # Path ke folder `asset`

    path = os.path.join(asset_dir, filename)
    if not os.path.exists(path):
        st.error(f"File tidak ditemukan: {path}")
        st.stop()
    return path
