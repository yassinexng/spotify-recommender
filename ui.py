import streamlit as st
import ast
import html

TOKENS = {
    "color": {
        "bg-page": "#080808",
        "bg-surface": "#0e0f0e",
        "bg-surface-raised": "#151715",
        "text-main": "#f2f4f2",
        "text-muted": "#9aa39a",
        "text-subtle": "#6b736b",
        "border-subtle": "#1e211e",
        "border-strong": "#2c302c",
        "primary": "#c7ffd0",
        "primary-hover": "#d8ffe0",
        "primary-active": "#b0f0bd",
        "on-primary": "#06120a",
        "state-danger": "#ff8a8a",
        "state-warning": "#f0d68a",
        "state-info": "#a8c8ff",
        "focus-ring": "#c7ffd0",
        "disabled": "#3a3f3a",
    },
    "space": {
        "4": "4px",
        "8": "8px",
        "12": "12px",
        "16": "16px",
        "20": "20px",
        "24": "24px",
        "32": "32px",
        "40": "40px",
        "48": "48px",
        "64": "64px",
    },
    "radius": {
        "sm": "6px",
        "md": "10px",
        "lg": "14px",
        "xl": "20px",
        "pill": "999px",
    },
    "type": {
        "display": "clamp(2rem, 4vw, 3rem)",
        "h1": "1.75rem",
        "h2": "1.25rem",
        "h3": "1rem",
        "body": "0.9375rem",
        "body-small": "0.8125rem",
        "label": "0.75rem",
        "caption": "0.6875rem",
        "code": "0.8125rem",
    },
    "elevation": {
        "menu": "0 8px 24px rgba(0,0,0,0.5), 0 0 0 1px var(--color-border-strong)",
    },
}


def build_css() -> str:
    lines = [":root {"]
    for group, items in TOKENS.items():
        for key, val in items.items():
            lines.append(f"    --{group}-{key}: {val};")
    lines.append("}")

    rules = """
    html, body, [class*="css"] {
        background-color: var(--color-bg-page);
        color: var(--color-text-main);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    .stApp {
        background-color: var(--color-bg-page);
    }
    .block-container {
        max-width: 1400px;
        margin-inline: auto;
        padding-top: var(--space-40);
        padding-bottom: var(--space-64);
        padding-inline: var(--space-24);
    }
    @media (max-width: 640px) {
        .block-container {
            padding-inline: var(--space-16);
            padding-top: var(--space-24);
        }
    }

    .section {
        margin-bottom: var(--space-64);
    }
    .section-inner {
        margin-bottom: var(--space-32);
    }
    .card {
        margin-bottom: var(--space-16);
    }

    :focus-visible {
        outline: 2px solid var(--color-focus-ring) !important;
        outline-offset: 2px !important;
        border-radius: inherit;
    }

    .t-display {
        font-size: var(--type-display);
        font-weight: 600;
        line-height: 1.1;
        letter-spacing: -0.02em;
        color: var(--color-text-main);
    }
    .t-h1 {
        font-size: var(--type-h1);
        font-weight: 600;
        line-height: 1.2;
        color: var(--color-text-main);
    }
    .t-h2 {
        font-size: var(--type-h2);
        font-weight: 600;
        line-height: 1.3;
        color: var(--color-text-main);
    }
    .t-h3 {
        font-size: var(--type-h3);
        font-weight: 600;
        line-height: 1.4;
        color: var(--color-text-main);
    }
    .t-body {
        font-size: var(--type-body);
        font-weight: 400;
        line-height: 1.55;
        color: var(--color-text-main);
    }
    .t-body-small {
        font-size: var(--type-body-small);
        font-weight: 400;
        line-height: 1.5;
        color: var(--color-text-muted);
    }
    .t-label {
        font-size: var(--type-label);
        font-weight: 500;
        line-height: 1.4;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        color: var(--color-text-muted);
    }
    .t-caption {
        font-size: var(--type-caption);
        font-weight: 400;
        line-height: 1.4;
        color: var(--color-text-subtle);
    }
    .t-code, .tabular-nums {
        font-size: var(--type-code);
        font-variant-numeric: tabular-nums;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.001ms !important;
            transition-duration: 0.001ms !important;
        }
    }

    .hero {
        position: relative;
        overflow: hidden;
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-xl);
        padding: var(--space-40) var(--space-48);
        margin-bottom: var(--space-32);
    }
    @media (max-width: 640px) {
        .hero {
            padding: var(--space-24) var(--space-20);
        }
    }
    .hero-glow {
        position: absolute;
        top: 0;
        right: 0;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle at top right, rgba(199, 255, 208, 0.06), transparent 70%);
        pointer-events: none;
    }
    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 640px;
    }

    .section-header-wrap {
        display: flex;
        align-items: center;
        gap: var(--space-16);
        margin-top: var(--space-48);
        margin-bottom: var(--space-24);
    }
    .section-header-line {
        flex: 1;
        height: 1px;
        background-color: var(--color-border-subtle);
    }

    .panel {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-lg);
        padding: var(--space-20);
        margin-bottom: var(--space-16);
    }
    .panel-heading {
        margin-bottom: var(--space-16);
    }

    .track-card {
        display: grid;
        grid-template-columns: 32px 1fr auto;
        align-items: flex-start;
        gap: var(--space-16);
        padding: var(--space-16);
        border-radius: var(--radius-md);
        border: 1px solid var(--color-border-subtle);
        background-color: var(--color-bg-surface);
        margin-bottom: var(--space-8);
        transition: background-color 0.15s ease, border-color 0.15s ease;
    }
    .track-card:hover {
        background-color: var(--color-bg-surface-raised);
        border-color: var(--color-border-strong);
    }
    .track-badge {
        width: 28px;
        height: 28px;
        border-radius: var(--radius-pill);
        border: 1px solid var(--color-border-subtle);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: var(--type-caption);
        color: var(--color-text-muted);
        font-variant-numeric: tabular-nums;
        background-color: var(--color-bg-page);
        margin-top: 2px;
    }
    .track-main {
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: var(--space-4);
    }
    .track-title {
        font-size: var(--type-body);
        font-weight: 500;
        color: var(--color-text-main);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.3;
    }
    .track-artist-pill {
        display: inline-flex;
        align-items: center;
        align-self: flex-start;
        font-size: var(--type-body-small);
        color: var(--color-text-muted);
        background-color: var(--color-bg-surface-raised);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-pill);
        padding: 2px var(--space-8);
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-4);
        margin-top: var(--space-4);
    }
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        font-size: var(--type-caption);
        color: var(--color-text-muted);
        background-color: var(--color-bg-surface-raised);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-pill);
        padding: 1px var(--space-8);
        line-height: 1.5;
    }
    .chip-key {
        color: var(--color-text-subtle);
        font-weight: 400;
    }
    .chip-val {
        color: var(--color-text-main);
        font-weight: 500;
    }

    .match-pill {
        display: inline-flex;
        align-items: center;
        background: rgba(199, 255, 208, 0.12);
        color: var(--color-primary);
        border: 1px solid rgba(199, 255, 208, 0.25);
        border-radius: var(--radius-pill);
        padding: 6px var(--space-12);
        font-size: var(--type-caption);
        font-weight: 600;
        font-variant-numeric: tabular-nums;
        white-space: nowrap;
        margin-top: 2px;
    }

    .auth-panel {
        max-width: 420px;
        margin: var(--space-32) auto;
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-lg);
        padding: var(--space-40);
        text-align: center;
    }
    .auth-dot {
        width: 32px;
        height: 32px;
        border-radius: var(--radius-pill);
        border: 2px solid var(--color-primary);
        background: rgba(199, 255, 208, 0.12);
        margin: 0 auto var(--space-20) auto;
    }

    .error-banner {
        display: flex;
        align-items: flex-start;
        gap: var(--space-12);
        background-color: rgba(255, 138, 138, 0.08);
        border: 1px solid var(--color-state-danger);
        border-radius: var(--radius-md);
        padding: var(--space-12) var(--space-16);
        margin-bottom: var(--space-16);
        color: var(--color-state-danger);
        font-size: var(--type-body-small);
        line-height: 1.4;
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--space-48) var(--space-24);
        text-align: center;
        background-color: var(--color-bg-surface);
        border: 1px dashed var(--color-border-subtle);
        border-radius: var(--radius-lg);
        margin-bottom: var(--space-16);
    }
    .empty-state-icon {
        color: var(--color-text-subtle);
        margin-bottom: var(--space-12);
    }

    .skeleton-line {
        height: 16px;
        background: linear-gradient(90deg, var(--color-bg-surface-raised) 25%, var(--color-border-subtle) 50%, var(--color-bg-surface-raised) 75%);
        background-size: 200% 100%;
        animation: skeleton-shimmer 1.8s infinite;
        border-radius: var(--radius-sm);
        margin-bottom: var(--space-8);
    }
    .skeleton-card {
        padding: var(--space-16);
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-md);
        margin-bottom: var(--space-8);
    }
    @keyframes skeleton-shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid var(--color-border-subtle);
        gap: var(--space-24);
        padding-bottom: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--color-text-muted);
        border: none;
        padding: var(--space-12) var(--space-16);
        font-size: var(--type-label);
        font-weight: 500;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        border-radius: 0;
    }
    .stTabs [aria-selected="true"] {
        color: var(--color-text-main) !important;
        background: transparent !important;
        box-shadow: inset 0 -2px 0 var(--color-primary) !important;
    }

    .stButton > button {
        background-color: var(--color-bg-surface-raised);
        color: var(--color-text-main);
        border: 1px solid var(--color-border-strong);
        border-radius: var(--radius-md);
        padding: var(--space-12) var(--space-20);
        font-size: var(--type-body);
        font-weight: 500;
        transition: background-color 0.15s ease, border-color 0.15s ease;
        width: 100%;
        min-height: 44px;
    }
    .stButton > button:hover {
        background-color: #1a1e1a;
        border-color: var(--color-primary);
        color: #ffffff;
    }
    .stButton > button:focus-visible {
        outline: 2px solid var(--color-focus-ring) !important;
        outline-offset: 2px !important;
    }

    .stLinkButton > a {
        background-color: var(--color-primary);
        color: var(--color-on-primary) !important;
        border: 1px solid var(--color-primary);
        border-radius: var(--radius-md);
        padding: var(--space-12) var(--space-24);
        font-size: var(--type-h3);
        font-weight: 600;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 44px;
        width: 100%;
        transition: background-color 0.15s ease;
    }
    .stLinkButton > a:hover {
        background-color: var(--color-primary-hover);
        color: var(--color-on-primary) !important;
    }
    .stLinkButton > a:active {
        background-color: var(--color-primary-active);
    }
    .stLinkButton > a:focus-visible {
        outline: 2px solid var(--color-focus-ring) !important;
        outline-offset: 2px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: var(--color-bg-surface-raised) !important;
        border: 1px solid var(--color-border-subtle) !important;
        border-radius: var(--radius-md) !important;
        color: var(--color-text-main) !important;
        min-height: 44px !important;
    }
    div[data-baseweb="select"]:focus-within > div {
        border-color: var(--color-focus-ring) !important;
        outline: 2px solid var(--color-focus-ring) !important;
        outline-offset: 2px !important;
    }
    div[data-baseweb="select"] svg {
        fill: var(--color-text-muted) !important;
    }

    div[data-testid="stDataFrame"] {
        background-color: var(--color-bg-surface);
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-lg);
        overflow: hidden;
        padding: var(--space-16);
    }
    div[data-testid="stDataFrame"] thead tr th {
        background-color: var(--color-bg-surface-raised) !important;
        color: var(--color-text-muted) !important;
        font-size: var(--type-label) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.02em !important;
        font-weight: 500 !important;
        border-bottom: 1px solid var(--color-border-subtle) !important;
    }
    div[data-testid="stDataFrame"] tbody tr td {
        background-color: var(--color-bg-surface) !important;
        color: var(--color-text-main) !important;
        border-bottom: 1px solid var(--color-border-subtle) !important;
    }
    div[data-testid="stDataFrame"] tbody tr:nth-child(even) td {
        background-color: rgba(21, 23, 21, 0.4) !important;
    }
    div[data-testid="stDataFrame"] tbody tr:hover td {
        background-color: var(--color-bg-surface-raised) !important;
    }
    """
    lines.append(rules)
    return "\n".join(lines)


def inject_global_styles() -> None:
    st.session_state["_styles_injected"] = True
    st.markdown(f"<style>{build_css()}</style>", unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-glow" aria-hidden="true"></div>
            <div class="hero-content">
                <div class="t-label" style="margin-bottom: var(--space-8);">Spotify Recommender</div>
                <div class="t-display" style="margin-bottom: var(--space-8);">Your taste, mapped.</div>
                <div class="t-body" style="color: var(--color-text-muted);">
                    Connects to your Spotify listening history and finds tracks that fit your profile.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = None) -> None:
    sub_html = f'<span class="t-caption" style="margin-left: var(--space-8);">{html.escape(subtitle)}</span>' if subtitle else ""
    st.markdown(
        f"""
        <div class="section-header-wrap">
            <span class="t-label">{html.escape(title)}</span>{sub_html}
            <div class="section-header-line" aria-hidden="true"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_match_pill(similarity: float) -> str:
    sim_val = round(similarity)
    return (
        f'<div class="match-pill" role="status" aria-label="Match score {sim_val} percent">'
        f'({sim_val}% match)'
        f'</div>'
    )


def _safe_parse_list(val):
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    if isinstance(val, str):
        val_str = val.strip()
        if val_str.startswith("[") and val_str.endswith("]"):
            try:
                parsed = ast.literal_eval(val_str)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                pass
        return [x.strip() for x in val_str.split(",") if x.strip()]
    if val is None:
        return []
    return [str(val).strip()]


def render_track_card(rank: int, title: str, artists, album: str = None, genres=None, audio_features: dict = None, similarity: float = 0.0) -> None:
    safe_title = html.escape(str(title or "Unknown Title"))
    parsed_artists = _safe_parse_list(artists)
    artist_display = ", ".join(parsed_artists) if parsed_artists else "Unknown Artist"
    safe_artist = html.escape(artist_display)

    chips = []
    if album and str(album).strip() and str(album).strip() not in ("['']", '[""]'):
        chips.append(f'<span class="chip"><span class="chip-key">Album</span> <span class="chip-val">{html.escape(str(album))}</span></span>')

    parsed_genres = _safe_parse_list(genres)
    for i, g in enumerate(parsed_genres, 1):
        chips.append(f'<span class="chip"><span class="chip-key">Genre {i}</span> <span class="chip-val">{html.escape(g)}</span></span>')

    chips_html = f'<div class="meta-row">{"".join(chips)}</div>' if chips else ""
    pill_html = render_match_pill(similarity)

    card_html = f"""
    <div class="track-card">
        <div class="track-badge">{rank}</div>
        <div class="track-main">
            <div class="track-title" title="{safe_title}">{safe_title}</div>
            <div class="track-artist-pill" title="{safe_artist}">{safe_artist}</div>
            {chips_html}
        </div>
        <div style="flex-shrink:0;">
            {pill_html}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_empty_state(message: str, action_label: str = None) -> bool:
    icon_svg = (
        '<svg class="empty-state-icon" width="32" height="32" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<circle cx="12" cy="12" r="10"/><path d="M10 12a2 2 0 1 0 4 0 2 2 0 0 0-4 0Z"/>'
        '<path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/>'
        '</svg>'
    )
    st.markdown(
        f"""
        <div class="empty-state">
            {icon_svg}
            <div class="t-body" style="color: var(--color-text-muted); max-width: 380px;">{html.escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if action_label:
        return st.button(action_label, key=f"empty_action_{message[:10]}")
    return False


def render_error_banner(message: str, retry_label: str = None) -> bool:
    alert_icon = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
        'style="flex-shrink:0; margin-top:2px;">'
        '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'
        '</svg>'
    )
    st.markdown(
        f"""
        <div class="error-banner" role="alert">
            {alert_icon}
            <div>{html.escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if retry_label:
        return st.button(retry_label, key=f"retry_{message[:10]}")
    return False


def render_loading_skeleton(kind: str = "cards") -> None:
    if kind == "table":
        st.markdown(
            """
            <div class="panel">
                <div class="skeleton-line" style="width: 100%; height: 28px;"></div>
                <div class="skeleton-line" style="width: 100%; height: 24px;"></div>
                <div class="skeleton-line" style="width: 100%; height: 24px;"></div>
                <div class="skeleton-line" style="width: 100%; height: 24px;"></div>
                <div class="skeleton-line" style="width: 100%; height: 24px;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="skeleton-card"><div class="skeleton-line" style="width: 40%;"></div><div class="skeleton-line" style="width: 70%;"></div></div>
            <div class="skeleton-card"><div class="skeleton-line" style="width: 35%;"></div><div class="skeleton-line" style="width: 65%;"></div></div>
            <div class="skeleton-card"><div class="skeleton-line" style="width: 50%;"></div><div class="skeleton-line" style="width: 80%;"></div></div>
            """,
            unsafe_allow_html=True,
        )


def _unpack_track(track):
    if isinstance(track, dict):
        return (
            track.get("title", ""),
            track.get("artists", []),
            track.get("album", ""),
            track.get("genres", []),
            track.get("audio_features", {}),
            float(track.get("similarity", 0.0)),
        )
    if isinstance(track, (list, tuple)):
        title = track[0] if len(track) > 0 else ""
        artists = track[1] if len(track) > 1 else []
        similarity = float(track[2]) if len(track) > 2 else 0.0
        album = track[3] if len(track) > 3 else ""
        genres = track[4] if len(track) > 4 else []
        features = track[5] if len(track) > 5 else {}
        return title, artists, album, genres, features, similarity
    return str(track), [], "", [], {}, 0.0


def render_recommendation_panel(heading: str, tracks: list) -> None:
    st.markdown(
        f"""
        <div class="panel">
            <div class="t-h2 panel-heading">{html.escape(heading)}</div>
        """,
        unsafe_allow_html=True,
    )
    if not tracks:
        render_empty_state("No recommendations calculated yet.")
    else:
        for i, item in enumerate(tracks, start=1):
            title, artists, album, genres, features, similarity = _unpack_track(item)
            render_track_card(
                rank=i,
                title=title,
                artists=artists,
                album=album,
                genres=genres,
                audio_features=features,
                similarity=similarity,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def render_results_panel(song_name: str, tracks: list) -> None:
    heading = f"Similar to {song_name}"
    render_recommendation_panel(heading, tracks)


def render_auth_panel(on_authorize, loading: bool = False, error: str = None) -> None:
    if error:
        render_error_banner(error)

    st.markdown(
        """
        <div class="auth-panel">
            <div class="auth-dot" aria-hidden="true"></div>
            <div class="t-h2" style="margin-bottom: var(--space-8);">Connect your Spotify account</div>
            <div class="t-body" style="color: var(--color-text-muted); margin-bottom: var(--space-24);">
                Authorize the app to read your top tracks and discover audio matches. Listening data remains local to your environment.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if loading:
            st.button("Authorizing…", disabled=True, key="auth_btn_loading")
        elif isinstance(on_authorize, str):
            st.link_button("Authorize with Spotify", on_authorize, use_container_width=True)
        elif callable(on_authorize):
            if st.button("Authorize with Spotify", key="auth_btn_callable", use_container_width=True):
                on_authorize()


def format_display_df(df):
    if df is None or len(df) == 0:
        return df
    if "Rank" in df.columns and "Artist" in df.columns and "Genres" in df.columns:
        return df
    import pandas as pd
    out = pd.DataFrame()
    out["Rank"] = range(1, len(df) + 1)
    out["Song"] = df["Song"].values if "Song" in df.columns else ""
    out["Artist"] = [", ".join(_safe_parse_list(a)) if _safe_parse_list(a) else "Unknown Artist" for a in df["artist(s)"]] if "artist(s)" in df.columns else ""
    out["Album"] = ["" if (isinstance(x, str) and x.strip() in ("", "['']", '[""]')) else (x if x is not None else "") for x in df["album_name"]] if "album_name" in df.columns else ""
    out["Genres"] = [", ".join(_safe_parse_list(g)) for g in df["genre(s)"]] if "genre(s)" in df.columns else ""
    return out


def render_tabs_and_tables(short_term_df, long_term_df) -> None:
    tab1, tab2 = st.tabs(["Short Term", "Long Term"])

    col_cfg = {
        "Rank": st.column_config.NumberColumn("Rank", width="small"),
        "Song": st.column_config.TextColumn("Song", width="medium"),
        "Artist": st.column_config.TextColumn("Artist", width="medium"),
        "Album": st.column_config.TextColumn("Album", width="medium"),
        "Genres": st.column_config.TextColumn("Genres", width="large"),
    }

    display_short = format_display_df(short_term_df)
    display_long = format_display_df(long_term_df)

    with tab1:
        if display_short is None or len(display_short) == 0:
            render_empty_state("No tracks found for short term listening.")
        else:
            st.dataframe(
                display_short,
                hide_index=True,
                use_container_width=True,
                column_config=col_cfg,
            )

    with tab2:
        if display_long is None or len(display_long) == 0:
            render_empty_state("No tracks found for long term listening.")
        else:
            st.dataframe(
                display_long,
                hide_index=True,
                use_container_width=True,
                column_config=col_cfg,
            )


def render_pick_a_track(
    title: str = "Pick a track from your top 15",
    subtitle: str = "Select any track to compute nearest audio neighbours.",
    top_tracks: list = None,
    on_find_similar = None,
    selected_song: str = None,
    key_prefix: str = "song_picker",
    loading: bool = False,
    error: str = None,
) -> str:
    st.markdown(
        f"""
        <div class="panel">
            <div class="t-h2 panel-heading">{html.escape(title)}</div>
            <div class="t-body" style="color: var(--color-text-muted); margin-bottom: var(--space-16);">
                {html.escape(subtitle)}
            </div>
        """,
        unsafe_allow_html=True,
    )

    if error:
        render_error_banner(error)

    tracks = top_tracks or []
    if not tracks:
        render_empty_state("No top tracks available to pick from.")
        st.markdown("</div>", unsafe_allow_html=True)
        return ""

    choice = st.selectbox(
        title,
        tracks,
        index=tracks.index(selected_song) if selected_song in tracks else 0,
        key=f"{key_prefix}_select",
        label_visibility="collapsed",
    )

    if loading:
        st.button("Finding similar songs…", disabled=True, key=f"{key_prefix}_loading")
    else:
        if st.button("Find similar songs", key=f"{key_prefix}_btn"):
            if callable(on_find_similar):
                on_find_similar(choice)

    st.markdown("</div>", unsafe_allow_html=True)
    return choice


def render_full_page(
    authed: bool,
    on_authorize=None,
    short_term_df=None,
    long_term_df=None,
    top1_tracks=None,
    top3_tracks=None,
    short_term_recs=None,
    long_term_recs=None,
    short_1_recs=None,
    long_1_recs=None,
    short_10_recs=None,
    long_10_recs=None,
    top_tracks_for_picker=None,
    top15_short_tracks=None,
    top5_long_tracks=None,
    on_find_similar=None,
    on_find_similar_short=None,
    on_find_similar_long=None,
    selected_song=None,
    similar_tracks=None,
    selected_source=None,
    error=None,
    loading=None,
    **kwargs,
) -> None:
    loading_dict = loading if isinstance(loading, dict) else {}
    s1 = short_1_recs if short_1_recs is not None else (short_term_recs or top1_tracks or kwargs.get("top1_tracks", []))
    l1 = long_1_recs if long_1_recs is not None else (long_term_recs or top3_tracks or kwargs.get("top3_tracks", []))
    s10 = short_10_recs or []
    l10 = long_10_recs or []

    render_hero()

    if not authed:
        auth_err = error if isinstance(error, str) else (error.get("auth") if isinstance(error, dict) else None)
        render_auth_panel(
            on_authorize=on_authorize,
            loading=loading_dict.get("auth", False),
            error=auth_err,
        )
        return

    render_tabs_and_tables(short_term_df, long_term_df)

    render_section_header("Recommendations", subtitle="Closest matches in audio-feature space")
    if loading_dict.get("recommendations", False):
        render_loading_skeleton(kind="cards")
    else:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            render_recommendation_panel("Built from your #1 track (Short Term)", s1)
        with col2:
            render_recommendation_panel("Built from your #1 track (Long Term)", l1)

        if s10 or l10:
            col3, col4 = st.columns(2, gap="large")
            with col3:
                render_recommendation_panel("Built from your #10 track (Short Term)", s10)
            with col4:
                render_recommendation_panel("Built from your #10 track (Long Term)", l10)

    render_section_header("Pick a track", subtitle="Find similar tracks to your favourites")
    picker_err = error.get("picker") if isinstance(error, dict) else None

    short_picker_list = top15_short_tracks or top_tracks_for_picker or []
    long_picker_list = top5_long_tracks or []

    if long_picker_list:
        pcol1, pcol2 = st.columns(2, gap="large")
        with pcol1:
            render_pick_a_track(
                title="Pick a track from your top 15",
                subtitle="Select any track from your top short term listening",
                top_tracks=short_picker_list,
                on_find_similar=on_find_similar_short or on_find_similar,
                selected_song=selected_song if selected_source != "long" else None,
                key_prefix="picker_short",
                loading=loading_dict.get("picker_short", False),
                error=picker_err if selected_source != "long" else None,
            )
        with pcol2:
            render_pick_a_track(
                title="Pick a track from your top 5 (long term)",
                subtitle="Select any track from your all-time favourites",
                top_tracks=long_picker_list,
                on_find_similar=on_find_similar_long or on_find_similar,
                selected_song=selected_song if selected_source == "long" else None,
                key_prefix="picker_long",
                loading=loading_dict.get("picker_long", False),
                error=picker_err if selected_source == "long" else None,
            )
    else:
        render_pick_a_track(
            title="Pick a track from your top 15",
            subtitle="Select any track from your recent favourites",
            top_tracks=short_picker_list,
            on_find_similar=on_find_similar_short or on_find_similar,
            selected_song=selected_song,
            key_prefix="picker_short",
            loading=loading_dict.get("picker", False),
            error=picker_err,
        )

    if selected_song and similar_tracks:
        render_results_panel(selected_song, similar_tracks)

