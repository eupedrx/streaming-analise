from typing import Tuple, cast
import streamlit as st
import pandas as pd
import plotly.express as px

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Streaming Brasil — Análise de Dados",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');

    :root {
        --bg: #000000;
        --panel: #0B0C0A;
        --panel-strong: #12130F;
        --signal: #FF3B30;
        --text: #F2F2EF;
        --muted: #A7A9A3;
        --line: #2A2D27;
    }

    .stApp {
        color: var(--text);
        background: var(--bg);
        font-family: 'IBM Plex Mono', monospace;
        font-variant-numeric: tabular-nums;
    }

    .block-container {
        padding-top: 2.1rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }

    [data-testid="stSidebar"] {
        background: var(--panel);
        border-right: 1px solid var(--line);
        box-shadow: none;
    }

    [data-testid="stSidebar"] * {
        font-family: 'IBM Plex Mono', monospace;
    }

    [data-testid="stSidebar"] .material-icons,
    [data-testid="stSidebar"] .material-symbols-rounded,
    [data-testid="stSidebar"] .material-symbols-outlined,
    [data-testid="stSidebar"] [class*="material"],
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
    }

    [data-testid="stSidebar"] h1 {
        color: var(--text);
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0;
        text-shadow: none;
    }

    [data-testid="stMetric"] {
        min-height: 132px;
        padding: 1rem 1rem 0.9rem;
        background: var(--panel);
        border: 1px solid var(--line);
        border-left: 3px solid var(--signal);
        border-radius: 0;
        box-shadow: none;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.76rem;
    }

    [data-testid="stMetricValue"] {
        color: var(--text);
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.55rem;
        text-shadow: none;
    }

    div[data-testid="stPlotlyChart"] {
        padding: 0.8rem;
        background: var(--panel);
        border: 1px solid var(--line);
        box-shadow: none;
    }

    .stMultiSelect [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"],
    .stSlider {
        color: var(--text);
        font-family: 'IBM Plex Mono', monospace;
    }

    div[data-baseweb="select"] > div {
        background-color: var(--panel-strong);
        border-color: var(--line);
        border-radius: 0;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        box-shadow: none;
    }

    hr {
        border: 0;
        height: 1px;
        background: var(--line);
        margin: 1.6rem 0;
    }

    .main-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: clamp(2rem, 4vw, 3.8rem);
        font-weight: 700;
        color: var(--text);
        margin: 0;
        line-height: 1.05;
        text-shadow: none;
    }

    .subtitle {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        color: var(--muted);
        margin-top: 0.65rem;
        margin-bottom: 1.7rem;
        text-shadow: none;
    }

    .kpi-box {
        background: var(--panel);
        border-radius: 0;
        padding: 1rem 1.2rem;
        border-left: 4px solid var(--signal);
    }

    .section-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.24rem;
        font-weight: 700;
        color: var(--text);
        border-bottom: 1px solid var(--line);
        padding-bottom: 0.55rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        text-shadow: none;
    }

    .insight-box {
        background: var(--panel);
        border: 1px solid var(--line);
        border-left: 4px solid var(--signal);
        padding: 0.95rem 1rem;
        border-radius: 0;
        margin-top: 0.8rem;
        color: var(--text);
        font-size: 0.92rem;
        box-shadow: none;
    }

    .insight-box b {
        color: var(--signal);
    }

    .conclusion-box {
        background: var(--panel);
        border: 1px solid var(--line);
        border-left: 4px solid var(--signal);
        padding: 1.15rem 1.25rem;
        border-radius: 0;
        margin-top: 1rem;
        color: var(--text);
        box-shadow: none;
    }

    .conclusion-box b {
        color: var(--signal);
    }

    .sidebar-brand {
        padding: 0.9rem 0.85rem;
        margin-bottom: 1rem;
        border: 1px solid var(--line);
        border-left: 3px solid var(--signal);
        background: var(--panel-strong);
        box-shadow: none;
    }

    .sidebar-brand-title {
        display: block;
        color: var(--text);
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.1;
        text-shadow: none;
    }

    .sidebar-brand-subtitle {
        display: block;
        margin-top: 0.35rem;
        color: var(--muted);
        font-size: 0.72rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Carregamento dos dados ──────────────────────────────────────────────────
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    dados: pd.DataFrame = pd.read_csv("dados/simulacao_streaming_brasil.csv")  # type: ignore[assignment]
    dados["data"] = pd.to_datetime(dados["data"])
    meses_pt = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
                7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
    dados["mes_nome"] = dados["mes"].map(meses_pt)
    dados["trimestre"] = dados["data"].dt.to_period("Q").astype(str)
    return dados

df_original = carregar_dados()

STREAMING_COLORS = ["#FF3B30", "#D7D7D2", "#8C9088", "#5F635B", "#C0C2BC", "#343832"]
CHART_LAYOUT = {
    "font": {"family": "IBM Plex Mono, monospace", "color": "#F2F2EF"},
    "plot_bgcolor": "#0B0C0A",
    "paper_bgcolor": "#0B0C0A",
    "legend": {"font": {"color": "#F2F2EF"}},
    "margin": {"l": 20, "r": 20, "t": 30, "b": 20},
}


def aplicar_tema_grafico(fig):
    fig.update_layout(**CHART_LAYOUT)
    fig.update_xaxes(
        gridcolor="#2A2D27",
        linecolor="#2A2D27",
        tickfont={"color": "#A7A9A3"},
        title_font={"color": "#F2F2EF"},
    )
    fig.update_yaxes(
        gridcolor="#2A2D27",
        linecolor="#2A2D27",
        tickfont={"color": "#A7A9A3"},
        title_font={"color": "#F2F2EF"},
    )
    return fig

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">🎬 Análise de Streaming no Brasil</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Padrões de consumo em plataformas digitais · 2015 – 2024</p>', unsafe_allow_html=True)

st.markdown("---")

# ── Sidebar — Filtros ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-brand-title">Streaming Brasil</span>
        <span class="sidebar-brand-subtitle">2015 - 2024</span>
    </div>
    """, unsafe_allow_html=True)
    st.title("🎛️ Filtros")

    # Extraímos o min e max diretamente da série do Pandas e convertemos para int
    min_ano = int(df_original["ano"].min())
    max_ano = int(df_original["ano"].max())

    ano_range = cast(Tuple[int, int], st.slider(
        "Período (ano)",
        min_value=min_ano,
        max_value=max_ano,
        value=(min_ano, max_ano)
    ))

    meses_disponiveis = sorted(df_original["mes"].unique())
    meses_nomes = {1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
                   7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"}
    mes_sel = st.multiselect("Mês", options=meses_disponiveis,
                             format_func=lambda x: meses_nomes.get(x, str(x)),
                             default=meses_disponiveis)

    plataformas = sorted(df_original["plataforma"].unique())
    plat_sel = st.multiselect("Plataforma", plataformas, default=plataformas)

    categorias = sorted(df_original["categoria"].unique())
    cat_sel = st.multiselect("Categoria", categorias, default=categorias)

    generos = sorted(df_original["genero"].unique())
    gen_sel = st.multiselect("Gênero", generos, default=generos)

    titulos = sorted(df_original["titulo"].unique())
    tit_sel = st.multiselect("Conteúdo", titulos, default=titulos)

    st.markdown("---")
    st.caption("Projeto G2 · Tema 21 · Análise de Streaming")

# ── Aplicar filtros ─────────────────────────────────────────────────────────
ano_min: int = ano_range[0]
ano_max: int = ano_range[1]

df = df_original[
    (df_original["ano"] >= ano_min) &
    (df_original["ano"] <= ano_max) &
    (df_original["mes"].isin(mes_sel)) &
    (df_original["plataforma"].isin(plat_sel)) &
    (df_original["categoria"].isin(cat_sel)) &
    (df_original["genero"].isin(gen_sel)) &
    (df_original["titulo"].isin(tit_sel))
].copy()

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ── KPIs ────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Indicadores-Chave (KPIs)</p>', unsafe_allow_html=True)

total_reprod     = df["reproducoes"].sum()
receita_total    = df["receita_plataforma"].sum()
media_usuarios   = df["usuarios_ativos"].mean()
plat_top         = df.groupby("plataforma")["reproducoes"].sum().idxmax()
titulo_top       = df.groupby("titulo")["reproducoes"].sum().idxmax()
genero_top       = df.groupby("genero")["reproducoes"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("▶️ Total de Reproduções",  f"{total_reprod:,.0f}".replace(",", "."))
col2.metric("💰 Receita Total",         f"R$ {receita_total:,.0f}".replace(",", "."))
col3.metric("👥 Média Usuários Ativos", f"{media_usuarios:,.0f}".replace(",", "."))
col4.metric("🏆 Plataforma Líder",      plat_top)
col5.metric("🎬 Conteúdo Mais Visto",   titulo_top)
col6.metric("🎭 Gênero Mais Consumido", genero_top)

st.markdown("---")

# ── Gráfico 1 — Evolução temporal ──────────────────────────────────────────
st.markdown('<p class="section-title">📈 Evolução Temporal do Consumo</p>', unsafe_allow_html=True)

evolucao = df.groupby(["ano", "plataforma"])["reproducoes"].sum().reset_index()
fig_linha = px.line(
    evolucao, x="ano", y="reproducoes", color="plataforma",
    markers=True,
    labels={"ano": "Ano", "reproducoes": "Reproduções", "plataforma": "Plataforma"},
    color_discrete_sequence=STREAMING_COLORS,
)
fig_linha.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    legend_title="Plataforma", xaxis=dict(dtick=1),
    hovermode="x unified"
)
aplicar_tema_grafico(fig_linha)
st.plotly_chart(fig_linha, use_container_width=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> Observe o crescimento acumulado de cada plataforma ao longo da década. Plataformas com crescimento consistente indicam consolidação de base de assinantes.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Gráfico 2 — Barras por plataforma ─────────────────────────────────────
st.markdown('<p class="section-title">📊 Comparação entre Plataformas</p>', unsafe_allow_html=True)

col_b1, col_b2 = st.columns(2)

with col_b1:
    plat_reprod = df.groupby("plataforma")["reproducoes"].sum().reset_index().sort_values("reproducoes", ascending=False)
    fig_plat = px.bar(
        plat_reprod, x="plataforma", y="reproducoes", color="plataforma",
        labels={"plataforma": "Plataforma", "reproducoes": "Reproduções"},
        color_discrete_sequence=STREAMING_COLORS,
    )
    fig_plat.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)")
    aplicar_tema_grafico(fig_plat)
    st.plotly_chart(fig_plat, use_container_width=True)

with col_b2:
    plat_receita = df.groupby("plataforma")["receita_plataforma"].sum().reset_index().sort_values("receita_plataforma", ascending=False)
    fig_rec = px.bar(
        plat_receita, x="plataforma", y="receita_plataforma", color="plataforma",
        labels={"plataforma": "Plataforma", "receita_plataforma": "Receita (R$)"},
        color_discrete_sequence=STREAMING_COLORS,
    )
    fig_rec.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)")
    aplicar_tema_grafico(fig_rec)
    st.plotly_chart(fig_rec, use_container_width=True)

st.markdown('<div class="insight-box">💡 <b>Insight:</b> Compare a audiência com a receita gerada por plataforma. Diferenças entre esses rankings revelam distintos modelos de monetização (assinatura vs. publicidade).</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Gráfico 3 — Barras por gênero ─────────────────────────────────────────
st.markdown('<p class="section-title">🎭 Análise por Gênero</p>', unsafe_allow_html=True)

gen_data = df.groupby(["genero", "categoria"])["reproducoes"].sum().reset_index()
fig_gen = px.bar(
    gen_data, x="genero", y="reproducoes", color="categoria",
    barmode="group",
    labels={"genero": "Gênero", "reproducoes": "Reproduções", "categoria": "Categoria"},
    color_discrete_sequence=STREAMING_COLORS,
)
fig_gen.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      legend_title="Categoria")
aplicar_tema_grafico(fig_gen)
st.plotly_chart(fig_gen, use_container_width=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> A distribuição por gênero e categoria revela preferências culturais do público brasileiro. Gêneros dominantes em múltiplas categorias indicam tendências de consumo transversal.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Gráfico 4 — Heatmap de horário de pico ────────────────────────────────
st.markdown('<p class="section-title">🕐 Heatmap de Horários de Pico</p>', unsafe_allow_html=True)

heat_data = df.groupby(["plataforma", "horario_pico"])["reproducoes"].sum().reset_index()
heat_pivot = heat_data.pivot(index="plataforma", columns="horario_pico", values="reproducoes").fillna(0)
horarios_ordem = [h for h in ["08:00", "12:00", "18:00", "21:00"] if h in heat_pivot.columns]
heat_pivot = heat_pivot[horarios_ordem]

fig_heat = px.imshow(
    heat_pivot,
    labels=dict(x="Horário de Pico", y="Plataforma", color="Reproduções"),
    color_continuous_scale=["#0B0C0A", "#343832", "#8C9088", "#D7D7D2", "#FF3B30"],
    aspect="auto",
    text_auto=".2s",
)
fig_heat.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
aplicar_tema_grafico(fig_heat)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> Células mais escuras indicam maior concentração de audiência. Horários noturnos tendem a concentrar séries e filmes, enquanto manhãs e almoços favorecem música e podcasts.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Gráfico 5 — Dispersão avaliação x reproduções ─────────────────────────
st.markdown('<p class="section-title">🔍 Relação: Avaliação × Audiência</p>', unsafe_allow_html=True)

fig_disp = px.scatter(
    df, x="avaliacao_media", y="reproducoes",
    color="plataforma", size="usuarios_ativos",
    hover_data=["titulo", "genero", "ano"],
    labels={"avaliacao_media": "Avaliação Média (0-5)",
            "reproducoes": "Reproduções",
            "plataforma": "Plataforma"},
    color_discrete_sequence=STREAMING_COLORS,
    opacity=0.7,
)
fig_disp.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       legend_title="Plataforma")
aplicar_tema_grafico(fig_disp)
st.plotly_chart(fig_disp, use_container_width=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> Cada ponto representa um registro. O tamanho reflete os usuários ativos. Uma correlação positiva indicaria que conteúdos mais bem avaliados geram maior audiência — nem sempre verdadeiro no streaming.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Gráfico 6 — Crescimento de assinaturas ────────────────────────────────
st.markdown('<p class="section-title">📈 Crescimento de Assinaturas</p>', unsafe_allow_html=True)

assin = df.groupby(["ano", "plataforma"])["assinaturas"].sum().reset_index()
fig_assin = px.area(
    assin, x="ano", y="assinaturas", color="plataforma",
    labels={"ano": "Ano", "assinaturas": "Assinaturas", "plataforma": "Plataforma"},
    color_discrete_sequence=STREAMING_COLORS,
)
fig_assin.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        hovermode="x unified", legend_title="Plataforma",
                        xaxis=dict(dtick=1))
aplicar_tema_grafico(fig_assin)
st.plotly_chart(fig_assin, use_container_width=True)
st.markdown('<div class="insight-box">💡 <b>Insight:</b> O gráfico de área empilhada evidencia o crescimento relativo de cada plataforma. Inclinações acentuadas indicam períodos de expansão acelerada de base de assinantes.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Tabela dinâmica ────────────────────────────────────────────────────────
st.markdown('<p class="section-title">📋 Tabela Dinâmica — Exploração Detalhada</p>', unsafe_allow_html=True)

agg_cols = st.multiselect(
    "Agrupar por:",
    ["plataforma", "categoria", "genero", "titulo", "ano", "mes_nome", "horario_pico"],
    default=["plataforma", "categoria"]
)

if agg_cols:
    tabela = df.groupby(agg_cols).agg(
        Reproducoes=("reproducoes", "sum"),
        Receita=("receita_plataforma", "sum"),
        Usuarios_Ativos=("usuarios_ativos", "mean"),
        Assinaturas=("assinaturas", "sum"),
        Avaliacao_Media=("avaliacao_media", "mean"),
    ).round(2).reset_index().sort_values("Reproducoes", ascending=False)

    tabela["Receita"]        = tabela["Receita"].apply(lambda x: f"R$ {x:,.2f}")
    tabela["Usuarios_Ativos"] = tabela["Usuarios_Ativos"].apply(lambda x: f"{x:,.0f}")
    tabela["Assinaturas"]    = tabela["Assinaturas"].apply(lambda x: f"{x:,.0f}")
    tabela["Reproducoes"]    = tabela["Reproducoes"].apply(lambda x: f"{x:,.0f}")

    st.dataframe(tabela, use_container_width=True, height=350)
else:
    st.info("Selecione ao menos uma coluna para agrupar.")

st.markdown("---")

# ── Interpretações Finais ────────────────────────────────────────────────────
st.markdown('<p class="section-title">Interpretações Finais</p>', unsafe_allow_html=True)

plat_receita_top = df.groupby("plataforma")["receita_plataforma"].sum().idxmax()
genero_mais = df.groupby("genero")["reproducoes"].sum().idxmax()
horario_mais = df.groupby("horario_pico")["reproducoes"].sum().idxmax()
ano_pico = df.groupby("ano")["reproducoes"].sum().idxmax()
cat_top = df.groupby("categoria")["reproducoes"].sum().idxmax()

st.markdown(f"""
<div class="conclusion-box">
<b>📌 Síntese da Análise — Streaming no Brasil (2015–2024)</b><br><br>

Com base nos dados filtrados, os principais achados são:

<ul>
  <li>A plataforma <b>{plat_top}</b> liderou em audiência, enquanto <b>{plat_receita_top}</b> gerou a maior receita no período analisado.</li>
  <li>O conteúdo mais reproduzido foi <b>"{titulo_top}"</b>, e o gênero mais consumido foi <b>{genero_top}</b>.</li>
  <li>A categoria dominante foi <b>{cat_top}</b>, refletindo o perfil de consumo do público brasileiro.</li>
  <li>O horário de pico com maior audiência concentrou-se às <b>{horario_mais}</b>, indicando forte consumo no período noturno/vespertino.</li>
  <li>O ano de <b>{ano_pico}</b> registrou o maior volume de reproduções no intervalo selecionado.</li>
  <li>A análise de dispersão entre avaliação e audiência sugere que popularidade nem sempre é determinada pela qualidade percebida — fatores como marketing, catálogo exclusivo e sazonalidade têm papel relevante.</li>
</ul>

Esses padrões são essenciais para orientar decisões estratégicas de plataformas, produtoras e anunciantes no mercado digital brasileiro.
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("📊 Projeto G2 · Tema 21 · Análise de Streaming no Brasil · Dados simulados (2015–2024)")
st.caption("Pedro Guilherme Sena · @eupedrx · github.com/eupedrx")
