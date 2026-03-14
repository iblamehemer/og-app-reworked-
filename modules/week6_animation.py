"""
modules/week6_animation.py — Week 6: Animated Visuals Studio
Missing items added: downloadable GIF + animation style selector
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use("Agg")
import numpy as np
import io
from matplotlib.animation import FuncAnimation, PillowWriter
from utils.session import mark_done

ANIM_STYLES = ["Fade-in + Typewriter", "Slide-in Left", "Zoom + Reveal", "Wipe + Fade"]


def _render_frame(ax, frame, company, slogan, bg, accent, fg, style):
    ax.clear()
    ax.set_facecolor(bg)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ch = (company[0] if company else "B").upper()
    nm = (company or "BRAND").upper()[:10]
    logo_alpha = min(1.0, frame / 20)
    type_chars = max(0, int(((frame - 22) / 38) * len(slogan))) if frame > 22 else 0
    type_chars = min(type_chars, len(slogan))

    if style == "Slide-in Left":
        x_pos = max(5, 15 - frame * 0.5)
        ax.text(x_pos, 6.5, ch, ha="center", va="center", fontsize=52, color=accent, fontfamily="serif")
    elif style == "Zoom + Reveal":
        scale = min(52, 10 + frame * 0.7)
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=scale, color=accent, fontfamily="serif", alpha=logo_alpha)
    else:
        ax.text(5, 6.5, ch, ha="center", va="center", fontsize=52, color=accent, fontfamily="serif", fontstyle="italic", alpha=logo_alpha)

    ax.text(5, 4.2, f'"{slogan[:type_chars]}"', ha="center", va="center", fontsize=9, color=fg, fontstyle="italic")

    if frame > 50:
        reveal_alpha = min(1.0, (frame - 50) / 10)
        ax.text(5, 2.5, nm, ha="center", va="center", fontsize=8, color=accent,
                fontfamily="monospace", fontweight="bold", alpha=reveal_alpha)


def _generate_gif(company, slogan, bg, accent, fg, style) -> bytes:
    """Generate animation GIF and return as bytes."""
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    fig.patch.set_facecolor(bg)

    def animate(frame):
        _render_frame(ax, frame, company, slogan, bg, accent, fg, style)
        return []

    anim = FuncAnimation(fig, animate, frames=80, interval=50)
    buf = io.BytesIO()
    writer = PillowWriter(fps=20)
    anim.save(buf, writer=writer, dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf.read()


def render_animation():
    company = st.session_state.get("company", "Brand")
    slogans = st.session_state.get("slogans")
    sel_sl  = st.session_state.get("selected_slogan", 0)
    slogan  = slogans[sel_sl]["text"] if slogans and sel_sl is not None else "Built for what's next."
    palettes = st.session_state.get("palettes")
    sel_pal  = st.session_state.get("selected_palette", 0)
    pal = (palettes[sel_pal] if palettes and sel_pal is not None else {"colors": ["#1a1a18","#b8975a","#f5f0e8"]})
    bg, accent, fg = pal["colors"][0], pal["colors"][1], pal["colors"][2]

    st.info("**Animation Approach:** PyCairo renders logo + tagline layers as vector objects. Matplotlib FuncAnimation drives frame-by-frame timing. Export targets 1080×1080 GIF/MP4 at 20fps via Pillow/MoviePy.")

    c1, c2 = st.columns(2)
    with c1:
        anim_style = st.selectbox("Animation style", ANIM_STYLES,
                                   index=ANIM_STYLES.index(st.session_state.get("animation_style", ANIM_STYLES[0])))
        st.session_state.animation_style = anim_style
    with c2:
        preview_frame = st.slider("Preview frame", 0, 80, 30)

    # Static preview
    st.subheader("Frame Preview")
    fig, ax = plt.subplots(figsize=(5, 5))
    _render_frame(ax, preview_frame, company, slogan, bg, accent, fg, anim_style)
    fig.patch.set_facecolor(bg)
    fig.tight_layout(pad=0)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
    st.caption(f"Frame {preview_frame}/80 · ~{preview_frame/20:.1f}s · Style: {anim_style}")

    # Storyboard
    st.subheader("Storyboard")
    s1, s2, s3, s4 = st.columns(4)
    for col, timing, desc in zip([s1,s2,s3,s4],
        ["0–1s\n(Frames 0–20)","1–3s\n(Frames 20–58)","2.5–3s\n(Frames 50–60)","3–4s\n(Frames 60–80)"],
        ["Logo fades in\nOpacity 0→1","Tagline types\nCharacter by character","Brand name\n+ palette reveal","Hold complete\nframe"]):
        with col:
            st.markdown(f"**{timing}**")
            st.caption(desc)

    st.divider()

    # GIF generation + download
    st.subheader("Export Animation")
    st.caption("Generates 80-frame GIF (4s @ 20fps) — may take ~10 seconds")
    if st.button("▶ Generate & Download GIF", key="gen_gif"):
        with st.spinner("Rendering animation frames…"):
            gif_bytes = _generate_gif(company, slogan, bg, accent, fg, anim_style)
            st.session_state.gif_bytes = gif_bytes
            st.session_state.animation_ready = True
        st.success("Animation rendered!")

    if st.session_state.get("gif_bytes"):
        st.download_button(
            "⬇ Download Animation GIF",
            data=st.session_state.gif_bytes,
            file_name=f"{company.replace(' ','_')}_animation.gif",
            mime="image/gif",
            use_container_width=True,
        )

    with st.expander("📄 PyCairo + Matplotlib Animation Code (Week 6)"):
        st.code("""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

fig, ax = plt.subplots(figsize=(10.8, 10.8), facecolor=bg_color)
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')

logo  = ax.text(5,6.5,ch,ha='center',va='center',fontsize=60,color=accent,alpha=0)
tag   = ax.text(5,4.2,'',ha='center',va='center',fontsize=10,color=fg,fontstyle='italic')
brand = ax.text(5,2.5,'',ha='center',va='center',fontsize=8,color=accent,fontweight='bold')

def animate(frame):
    logo.set_alpha(min(1.0, frame/20))
    if frame > 22:
        n = int(((frame-22)/38)*len(slogan))
        tag.set_text(slogan[:n])
    if frame > 50:
        brand.set_text(company.upper())
        brand.set_alpha(min(1.0,(frame-50)/10))
    return logo, tag, brand

anim = FuncAnimation(fig, animate, frames=80, interval=50, blit=True)
anim.save('brand_animation.gif', writer=PillowWriter(fps=20), dpi=100)
""", language="python")

    if st.button("Continue to Campaign Studio →", key="anim_next"):
        mark_done("W6")
        st.success("Animation configured! Move to the **Campaign** tab.")
