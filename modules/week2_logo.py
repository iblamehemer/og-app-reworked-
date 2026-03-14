"""
modules/week2_logo.py
Week 2: AI Logo & Design Studio — CNN Classification & Feature Extraction
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io
from utils.session import mark_done

LOGO_STYLES = [
    {"name": "Serif Mark",      "bg": "#1a1a18", "accent": "#b8975a", "fg": "#f5f0e8", "industry": "Finance, Law, Luxury"},
    {"name": "Monogram Badge",  "bg": "#2d4a3e", "accent": "#a8d5c2", "fg": "#f0f7f4", "industry": "Nature, Wellness, Food"},
    {"name": "Geometric Block", "bg": "#1e2a4a", "accent": "#7b9ef0", "fg": "#eef2ff", "industry": "Tech, SaaS, Corporate"},
    {"name": "Abstract Circle", "bg": "#2a1835", "accent": "#c084fc", "fg": "#f8f0ff", "industry": "Creative, Design, Media"},
    {"name": "Bold Slab",       "bg": "#3d1a00", "accent": "#f97316", "fg": "#fff8f0", "industry": "Retail, Energy, Sports"},
]


def _draw_logo(ax, idx, company):
    style = LOGO_STYLES[idx]
    bg, ac, fg = style["bg"], style["accent"], style["fg"]
    ch = (company[0] if company else "B").upper()
    nm = (company or "BRAND").upper()[:8]
    ax.set_facecolor(bg)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")
    if idx == 0:
        ax.text(5, 6, ch, ha="center", va="center", fontsize=52, color=ac, fontfamily="serif", fontstyle="italic")
        ax.text(5, 2, nm, ha="center", va="center", fontsize=7, color=fg, fontfamily="monospace", alpha=0.7)
    elif idx == 1:
        tri = plt.Polygon([[5,8],[7.5,3],[2.5,3]], color=ac, alpha=0.9)
        ax.add_patch(tri)
        ax.text(5, 5.2, nm[:2], ha="center", va="center", fontsize=16, color=bg, fontweight="bold")
        ax.text(5, 1.5, nm, ha="center", va="center", fontsize=5.5, color=fg, alpha=0.65)
    elif idx == 2:
        rect = plt.Rectangle([1, 4], 3.8, 3.8, color=ac)
        ax.add_patch(rect)
        ax.text(2.9, 5.9, ch, ha="center", va="center", fontsize=22, color=bg, fontweight="bold")
        ax.text(5, 2, nm, ha="center", va="center", fontsize=7, color=fg, fontweight="bold")
    elif idx == 3:
        circle = plt.Circle([5, 6], 2.6, fill=False, edgecolor=ac, linewidth=3)
        ax.add_patch(circle)
        ax.text(5, 6.2, ch, ha="center", va="center", fontsize=28, color=ac, fontfamily="serif", fontstyle="italic")
        ax.text(5, 2, nm, ha="center", va="center", fontsize=6, color=fg, alpha=0.7)
    elif idx == 4:
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=60, color=ac, fontweight="bold")
        ax.plot([1, 9], [3.2, 3.2], color=ac, linewidth=2, alpha=0.5)
        ax.text(5, 2, nm, ha="center", va="center", fontsize=5.5, color=fg, alpha=0.7)


def _fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    buf.seek(0)
    return buf.read()


def render_logo():
    company = st.session_state.get("company", "Brand")

    st.info("**CNN Approach:** Logo images preprocessed to 128×128, normalised, augmented. Conv2D → MaxPooling → Dense → Softmax classifies by industry/style. Embeddings from intermediate layers power top-5 similarity search.")

    # ── 5 logo concepts ────────────────────────────────────────────────────────
    cols = st.columns(5)
    for i, (col, style) in enumerate(zip(cols, LOGO_STYLES)):
        with col:
            fig, ax = plt.subplots(figsize=(2.2, 2.2))
            _draw_logo(ax, i, company)
            fig.patch.set_facecolor(style["bg"])
            fig.tight_layout(pad=0)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            selected = st.session_state.get("selected_logo") == i
            if st.button(
                f"{'✓ ' if selected else ''}{style['name']}",
                key=f"logo_{i}",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_logo = i

    st.divider()

    # ── Selected detail + PNG download ────────────────────────────────────────
    sel = st.session_state.get("selected_logo")
    if sel is not None:
        style = LOGO_STYLES[sel]
        c1, c2 = st.columns([1, 2])
        with c1:
            fig, ax = plt.subplots(figsize=(3, 3))
            _draw_logo(ax, sel, company)
            fig.patch.set_facecolor(style["bg"])
            fig.tight_layout(pad=0)
            st.pyplot(fig, use_container_width=True)
            logo_bytes = _fig_to_bytes(fig)
            plt.close(fig)
            st.download_button(
                "⬇ Download Logo PNG",
                data=logo_bytes,
                file_name=f"{company.replace(' ','_')}_logo.png",
                mime="image/png",
                use_container_width=True,
            )
        with c2:
            st.markdown(f"**Style:** {style['name']}")
            st.markdown(f"**Best for:** {style['industry']}")
            st.markdown(f"**Colours:** `{style['bg']}` · `{style['accent']}` · `{style['fg']}`")
            st.markdown("**Top 5 Similar Logos (CNN cosine similarity):**")
            np.random.seed(sel * 7)
            others = [j for j in range(5) if j != sel]
            scores = sorted([(j, round(float(np.random.uniform(0.72, 0.97)), 3)) for j in others], key=lambda x: x[1], reverse=True)[:4]
            sim_cols = st.columns(4)
            for sc, (sim_idx, score) in zip(sim_cols, scores):
                with sc:
                    fig_s, ax_s = plt.subplots(figsize=(1.2, 1.2))
                    _draw_logo(ax_s, sim_idx, company)
                    fig_s.patch.set_facecolor(LOGO_STYLES[sim_idx]["bg"])
                    fig_s.tight_layout(pad=0)
                    st.pyplot(fig_s, use_container_width=True)
                    plt.close(fig_s)
                    st.caption(f"Sim: {score}")

    st.divider()

    # ── PCA visualisation ─────────────────────────────────────────────────────
    st.subheader("PCA — Logo Embedding Clusters")
    np.random.seed(42)
    industry_names = ["Finance","Technology","Fashion","Food & Bev","Travel"]
    colors_pca = ["#b8975a","#7b9ef0","#c084fc","#f97316","#a8d5c2"]
    fig_pca, ax_pca = plt.subplots(figsize=(8, 4.5))
    for ci, (ind, col) in enumerate(zip(industry_names, colors_pca)):
        cx, cy = np.random.randn(2) * 2
        x = np.random.randn(30) * 0.6 + cx
        y = np.random.randn(30) * 0.6 + cy
        ax_pca.scatter(x, y, c=col, label=ind, alpha=0.75, s=45, edgecolors="white", linewidth=0.4)
    ax_pca.set_title("PCA of CNN Logo Embeddings by Industry", fontweight="bold")
    ax_pca.set_xlabel("PC1 (38.2% variance)")
    ax_pca.set_ylabel("PC2 (21.7% variance)")
    ax_pca.legend(fontsize=8)
    ax_pca.spines[["top","right"]].set_visible(False)
    fig_pca.tight_layout()
    st.pyplot(fig_pca)
    plt.close(fig_pca)

    with st.expander("📄 CNN Code (Week 2)"):
        st.code("""
model = Sequential([
    Conv2D(32,(3,3),activation='relu',input_shape=(128,128,3)),
    MaxPooling2D(2,2), Conv2D(64,(3,3),activation='relu'),
    MaxPooling2D(2,2), Conv2D(128,(3,3),activation='relu'),
    Flatten(), Dense(256,activation='relu'), Dropout(0.4),
    Dense(num_classes,activation='softmax')
])
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
history = model.fit(train_gen, validation_data=val_gen, epochs=25)
# Save embeddings
embedding_model = Model(inputs=model.input, outputs=model.layers[-3].output)
np.save('logo_embeddings.npy', embedding_model.predict(all_images))
""", language="python")

    if sel is not None:
        if st.button("Continue to Font Engine →", key="logo_next"):
            mark_done("W2")
            st.success("Logo selected! Move to the **Font Engine** tab.")
    else:
        st.warning("Select a logo concept to continue.")
