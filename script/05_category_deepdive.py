import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import japanize_matplotlib
import matplotlib.ticker as mtick


# データ読み込み
df = pd.read_csv("../data/customer_shopping_data_2022.csv")

# 「invoice_date」を日付型に変換
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")


# 特に売上が高いカテゴリのデータを抽出
df_filtered = df[df["category"].isin(["Clothing", "Shoes", "Technology"])]


# カテゴリ×年代で売上高と取引件数を集計
sales_by_age = df_filtered.groupby(["category", "age_group"])["total_amount"].sum().unstack()
count_by_age = df_filtered.groupby(["category", "age_group"])["invoice_no"].count().unstack()


# カテゴリ×性別で売上高と取引件数を集計
sales_by_gender = df_filtered.groupby(["category", "gender"])["total_amount"].sum().unstack()
count_by_gender = df_filtered.groupby(["category", "gender"])["invoice_no"].count().unstack()



# グラフによる可視化

# 年代別
# 年代別カラー（5色）
age_colors = ["#c6dbef", "#9ecae1", "#6baed6", "#3182bd", "#08519c"]
figsize = (10, 6)
formatter = mtick.FuncFormatter(lambda x, _: f"{int(x):,}")

age_plots = [
    ("sales_by_age", "カテゴリ × 年代別の売上合計（2022年）", "age_sales"),
    ("count_by_age", "カテゴリ × 年代別の取引件数（2022年）", "age_count"),
]

for i, (var_name, title, filename) in enumerate(age_plots, start=16):
    df_plot = eval(var_name)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    df_plot.columns = ["10代", "20代", "30代", "40代", "50代", "60代以上"]
    df_plot.plot(kind="bar", ax=ax, color=age_colors, width=0.9)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel("カテゴリ", fontsize=12)
    ax.set_ylabel("合計売上（TL）" if "sales" in filename else "取引件数", fontsize=12)
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    plt.show()

    fig.savefig(f"../output/{i:02d}_{filename}.png", dpi=300, bbox_inches="tight")



# 性別
gender_colors = ["#f7c6c7", "#6ca0dc"]

gender_plots = [
    ("sales_by_gender", "カテゴリ × 性別別の売上合計（2022年）", "gender_sales"),
    ("count_by_gender", "カテゴリ × 性別別の取引件数（2022年）", "gender_count"),
]

for i, (var_name, title, filename) in enumerate(gender_plots, start=18):
    df_plot = eval(var_name)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    df_plot.columns = ["女性", "男性"]
    df_plot.plot(kind="bar", ax=ax, color=gender_colors)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel("カテゴリ", fontsize=12)
    ax.set_ylabel("合計売上（TL）" if "sales" in filename else "取引件数", fontsize=12)
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    plt.show()

    fig.savefig(f"../output/{i:02d}_{filename}.png", dpi=300, bbox_inches="tight")
