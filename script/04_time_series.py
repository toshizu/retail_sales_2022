import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import japanize_matplotlib
import matplotlib.ticker as mtick


# データ読み込み
df = pd.read_csv("../data/customer_shopping_data_2022.csv")

# 「invoice_date」を日付型に変換
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")


# 月列の作成
df["month"] = df["invoice_date"].dt.month


# 曜日列の作成
weekday_map = {
    0: "月",
    1: "火",
    2: "水",
    3: "木",
    4: "金",
    5: "土",
    6: "日"
}
df["weekday"] = df["invoice_date"].dt.weekday.map(weekday_map)
weekday_order = ["月", "火", "水", "木", "金", "土", "日"]


# 季節列の作成
def get_season(month):
    if month in [3, 4, 5]:
        return "春"
    elif month in [6, 7, 8]:
        return "夏"
    elif month in [9, 10, 11]:
        return "秋"
    else:
        return "冬"
df["season"] = df["month"].apply(get_season)
season_order = ["春", "夏", "秋", "冬"]


# 月別
monthly_summary = df.groupby("month").agg(
    total_sales = ("total_amount", "sum"),
    transaction_count = ("invoice_no", "count"))


# 曜日別
weekday_summary = df.groupby("weekday").agg(
    total_sales = ("total_amount", "sum"),
    transaction_count = ("invoice_no", "count")).reindex(weekday_order)


# 季節別
season_summary = df.groupby("season").agg(
    total_sales = ("total_amount", "sum"),
    transaction_count = ("invoice_no", "count")).reindex(season_order)


# グラフによる可視化

# 共通設定
figsize = (10, 6)
formatter = mtick.FuncFormatter(lambda x, _: f"{int(x):,}")

# 描画対象とファイル番号の定義
plot_targets = [
    ("monthly_summary", "month", "月別"),
    ("weekday_summary", "weekday", "曜日別"),
    ("season_summary", "season", "季節別")
]

# 通し番号のスタート
plot_cols = ["total_sales", "transaction_count"]
base_fig_num = 10

# 実行
for i, (df_name, x_label, title_prefix) in enumerate(plot_targets):
    df_obj = eval(df_name)
    for j, col in enumerate(plot_cols):
        fig_num = base_fig_num + i * 2 + j  # 通し番号 10〜15

        fig, ax = plt.subplots(figsize=figsize, facecolor="white")
        df_obj[col].plot(kind="bar", color="#9e9ac8", ax=ax)

        ax.set_title(f"{title_prefix}の{ '売上合計' if col == 'total_sales' else '取引件数' }（2022年）", fontsize=14)
        ax.set_xlabel(title_prefix, fontsize=12)
        ax.set_ylabel("合計売上（TL）" if col == "total_sales" else "取引件数", fontsize=12)
        ax.yaxis.set_major_formatter(formatter)
        ax.tick_params(axis="x", rotation=0)

        plt.tight_layout()
        plt.show()

        # 保存
        fig.savefig(f"../output/{fig_num:02d}_{x_label}_{col}.png", dpi=300, bbox_inches="tight")
