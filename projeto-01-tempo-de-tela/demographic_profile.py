import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ── Sample data (replace with your df) ────────────────────────────────────────
np.random.seed(42)
n = 3000
df = pd.DataFrame({
    'Age':        np.random.normal(35, 12, n).clip(18, 75).astype(int),
    'Gender':     np.random.choice(['Masculino', 'Feminino', 'Outro'], n, p=[0.48, 0.46, 0.06]),
    'Occupation': np.random.choice(
        ['Tecnologia', 'Saúde', 'Educação', 'Finanças', 'Varejo', 'Outros'],
        n, p=[0.25, 0.18, 0.15, 0.14, 0.13, 0.15]
    ),
})

# ── Design tokens ──────────────────────────────────────────────────────────────
BG        = '#0F1117'
CARD      = '#181C27'
GRID_C    = '#252A38'
TEXT_PRI  = '#F0F2FA'
TEXT_SEC  = '#7B82A0'
ACCENT    = '#5B8DEF'
PALETTE   = ['#5B8DEF', '#A78BFA', '#34D399', '#F472B6', '#FBBF24', '#60A5FA']
MEAN_C    = '#F472B6'

plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'text.color':        TEXT_PRI,
    'axes.facecolor':    CARD,
    'axes.edgecolor':    GRID_C,
    'axes.labelcolor':   TEXT_SEC,
    'axes.titlecolor':   TEXT_PRI,
    'axes.titlesize':    12,
    'axes.titleweight':  'bold',
    'axes.titlepad':     14,
    'axes.labelsize':    9,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'xtick.color':       TEXT_SEC,
    'ytick.color':       TEXT_SEC,
    'xtick.labelsize':   8,
    'ytick.labelsize':   8,
    'figure.facecolor':  BG,
    'grid.color':        GRID_C,
    'grid.linewidth':    0.6,
})

# ── Figure & layout ───────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 6.5))
fig.subplots_adjust(left=0.05, right=0.97, top=0.82, bottom=0.12, wspace=0.38)

gs = GridSpec(1, 3, figure=fig)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

# ── Header ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.96, 'PERFIL DEMOGRÁFICO DOS USUÁRIOS',
         ha='center', va='top', fontsize=15, fontweight='bold',
         color=TEXT_PRI)
fig.text(0.5, 0.90, f'Base: {len(df):,} usuários  ·  Última atualização: 2025',
         ha='center', va='top', fontsize=8.5, color=TEXT_SEC)

# thin accent line under title
fig.add_artist(plt.Line2D([0.22, 0.78], [0.885, 0.885],
               transform=fig.transFigure, color=ACCENT, linewidth=0.8, alpha=0.5))

# ── Chart 1 · Age Histogram ───────────────────────────────────────────────────
ages = df['Age']
bins = np.arange(ages.min(), ages.max() + 2, 2)

n_vals, edges, patches = ax1.hist(ages, bins=bins, color=ACCENT,
                                   edgecolor=BG, linewidth=0.4, zorder=3)

# gradient-like coloring by bin position
norm_vals = n_vals / n_vals.max()
for patch, nv in zip(patches, norm_vals):
    patch.set_alpha(0.45 + 0.55 * nv)

mean_age = ages.mean()
ax1.axvline(mean_age, color=MEAN_C, linewidth=1.6, linestyle='--', zorder=4)
ax1.text(mean_age + 0.6, ax1.get_ylim()[1] * 0.93,
         f'Média\n{mean_age:.1f}a', color=MEAN_C, fontsize=7.5,
         fontweight='bold', va='top')

ax1.set_title('Distribuição de Idade')
ax1.set_xlabel('Idade (anos)')
ax1.set_ylabel('Frequência')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax1.grid(axis='y', zorder=0)
ax1.set_axisbelow(True)

# ── Chart 2 · Gender Donut ────────────────────────────────────────────────────
gender_counts = df['Gender'].value_counts()
wedge_colors  = PALETTE[:len(gender_counts)]

wedges, texts, autotexts = ax2.pie(
    gender_counts,
    labels=None,
    autopct='%1.1f%%',
    colors=wedge_colors,
    startangle=90,
    pctdistance=0.75,
    wedgeprops={'edgecolor': BG, 'linewidth': 2.5, 'width': 0.52},   # donut
)

for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight('bold')
    at.set_color(TEXT_PRI)

# center label
ax2.text(0, 0, f'{len(df):,}\nusuários', ha='center', va='center',
         fontsize=9, color=TEXT_PRI, fontweight='bold', linespacing=1.5)

# custom legend inside axes
legend_patches = [
    mpatches.Patch(color=c, label=f'{lbl}  {cnt:,}')
    for c, lbl, cnt in zip(wedge_colors, gender_counts.index, gender_counts.values)
]
ax2.legend(handles=legend_patches, loc='lower center',
           bbox_to_anchor=(0.5, -0.14), ncol=len(gender_counts),
           frameon=False, fontsize=8, labelcolor=TEXT_SEC)
ax2.set_title('Distribuição por Gênero')

# ── Chart 3 · Occupation Bar ──────────────────────────────────────────────────
occ = df['Occupation'].value_counts().sort_values()
bar_colors = [PALETTE[i % len(PALETTE)] for i in range(len(occ))]

bars = ax3.barh(occ.index, occ.values, color=bar_colors,
                height=0.62, zorder=3)

# subtle background track
ax3.barh(occ.index, [occ.max() * 1.15] * len(occ),
         color=GRID_C, height=0.62, zorder=1, alpha=0.35)

for bar, val in zip(bars, occ.values):
    pct = val / len(df) * 100
    ax3.text(val + occ.max() * 0.02, bar.get_y() + bar.get_height() / 2,
             f'{val:,}  ({pct:.1f}%)', va='center', fontsize=8,
             color=TEXT_SEC)

ax3.set_title('Distribuição por Ocupação')
ax3.set_xlabel('Usuários')
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax3.set_xlim(0, occ.max() * 1.35)
ax3.grid(axis='x', zorder=0)
ax3.set_axisbelow(True)
ax3.tick_params(axis='y', length=0)
ax3.spines['left'].set_visible(False)

plt.savefig('/mnt/user-data/outputs/demographic_profile.png',
            dpi=160, bbox_inches='tight', facecolor=BG)
plt.show()
print("Saved → demographic_profile.png")
