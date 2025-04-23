
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from io import BytesIO

# --- descriptor + category + color 정의
descriptor_data = [
    ("uneasy", "Tension / Unease", (1.0, 0.2, 0.2, 1.0)),
    ("tense", "Tension / Unease", (1.0, 0.2, 0.2, 1.0)),
    ("anxious", "Tension / Unease", (1.0, 0.2, 0.2, 1.0)),
    ("melancholic", "Melancholy / Sentimentality", (0.2, 0.4, 1.0, 1.0)),
    ("nostalgic", "Melancholy / Sentimentality", (0.2, 0.4, 1.0, 1.0)),
    ("poignant", "Melancholy / Sentimentality", (0.2, 0.4, 1.0, 1.0)),
    ("still", "Stillness / Drift", (0.4, 0.6, 1.0, 1.0)),
    ("sublime", "Sublimity / Ominousness", (0.6, 0.2, 0.8, 1.0)),
    ("ominous", "Sublimity / Ominousness", (0.6, 0.2, 0.8, 1.0)),
    ("exposed", "Explicitness / Exposure", (1.0, 0.1, 0.1, 1.0)),
    ("intense", "Excess / Intensity", (0.9, 0.0, 0.1, 1.0)),
    ("playful", "Play / Lightness", (1.0, 0.9, 0.3, 1.0)),
    ("light", "Play / Lightness", (1.0, 0.9, 0.3, 1.0)),
    ("serious", "Gravitas / Seriousness", (0.5, 0.5, 0.5, 1.0)),
    ("weighty", "Gravitas / Seriousness", (0.5, 0.5, 0.5, 1.0)),
    ("strange", "Strangeness / Uncanny", (1.0, 0.5, 0.2, 1.0)),
    ("uncanny", "Strangeness / Uncanny", (1.0, 0.5, 0.2, 1.0)),
    ("meta", "meta-affect", (0.8, 0.4, 0.9, 1.0))
]
df = pd.DataFrame(descriptor_data, columns=["Descriptor", "Category", "Color"])
df["OptionLabel"] = df["Category"] + " - " + df["Descriptor"]

# --- Streamlit 앱 시작
st.set_page_config(layout="wide")
st.title("Affective Terrain Map Generator")

# --- 사용자 입력: descriptor 선택
selected_labels = st.multiselect(
    "Select Category - Descriptor (up to 10)",
    options=df["OptionLabel"].tolist(),
    default=df["OptionLabel"].tolist()[:4]
)

selected_descriptors = df[df["OptionLabel"].isin(selected_labels)]["Descriptor"].tolist()

# --- 지형 생성
width, height = 100, 100
canvas = np.zeros((height, width, 4))  # RGBA

np.random.seed(42)
for desc in selected_descriptors:
    row = df[df["Descriptor"] == desc].iloc[0]
    x, y = np.random.randint(20, 80), np.random.randint(20, 80)
    intensity_map = np.zeros((height, width))
    intensity_map[y, x] = 1.0
    blurred = gaussian_filter(intensity_map, sigma=12)
    color = row['Color']
    for i in range(4):
        canvas[:, :, i] += blurred * color[i]

# RGBA -> RGB 변환
rgb_canvas = canvas[:, :, :3]
for i in range(3):
    max_val = rgb_canvas[:, :, i].max()
    if max_val > 0:
        rgb_canvas[:, :, i] /= max_val

# --- 시각화 출력
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(rgb_canvas, origin='lower')
ax.set_title("Flow-based Affective Terrain Map")
ax.axis('off')
st.pyplot(fig)

# --- PNG 저장 버튼
buffer = BytesIO()
fig.savefig(buffer, format="png")
buffer.seek(0)
st.download_button(
    label="Download Affective Map as PNG",
    data=buffer,
    file_name="affective_map.png",
    mime="image/png"
)

# --- 선택된 descriptor와 정동 범주 표시
if st.checkbox("Show Selected Table"):
    display_df = df[df["Descriptor"].isin(selected_descriptors)].drop_duplicates()
    st.dataframe(display_df[['Category', 'Descriptor']].sort_values(by="Category"))
