import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import japanize_matplotlib
import matplotlib.ticker as mtick
import seaborn as sns


# データ読み込み
df = pd.read_csv("../data/customer_shopping_data_2022.csv")

# 「invoice_date」を日付型に変換
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")


# モール別の売上と取引件数を集計
mall_sales = df.groupby("shopping_mall").agg(
    total_sales = ("total_amount", "sum"),
    transaction_count = ("invoice_no", "count"),
    customer_count = ("customer_id", "nunique")
).sort_values("total_sales", ascending=False)


# 各集計項目を棒グラフで可視化

# グラフサイズ統一化
figsize = (10, 6)

# カンマ区切りのフォーマッター
formatter = mtick.FuncFormatter(lambda x, _: f"{int(x):,}")

# カラム名とタイトルの対応
plot_items = {
    "total_sales" : "モール別の売上合計(2022年)",
    "transaction_count" : "モール別の取引件数(2022年)"
}

# 各指標を個別に描画

for i, (col, title) in enumerate(plot_items.items(), start=4):
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    mall_sales[col].plot(kind="bar", color="#a1d99b", ax=ax)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel("ショッピングモール", fontsize=12)
    ax.set_ylabel("件数" if col != "total_sales" else "合計売上(TL)", fontsize=12)
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(f"../output/{i:02d}_mall_{col}.png", dpi=300, bbox_inches="tight")
    plt.show()



# カテゴリ別の売上と取引件数を集計
category_sales = df.groupby("category").agg(
    total_sales = ("total_amount", "sum"),
    transaction_count = ("invoice_no", "count"),
    customer_count = ("customer_id", "nunique")
).sort_values("total_sales", ascending=False)


# 集計結果を可視化

# グラフサイズ、フォーマッタ
figsize = (10, 6)
formatter = mtick.FuncFormatter(lambda x, _: f"{int(x):,}")

# 表示項目とタイトル
plot_items = {
    "total_sales" : "カテゴリ別の売上合計(2022年)",
    "transaction_count" : "カテゴリ別の取引件数(2022年)"
}

# グラフの描画と保存
for i, (col, title) in enumerate(plot_items.items(), start=6):
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    category_sales[col].plot(kind="bar", color="#fdae6b", ax=ax)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel("商品カテゴリ", fontsize=12)
    ax.set_ylabel("合計金額(TL)" if col == "total_sales" else "件数", fontsize=12,)
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    fig.savefig(f"../output/{i:02d}_category_{col}.png", dpi=300, bbox_inches="tight")
    plt.show()


# モール別×カテゴリ別のクロス集計
# 合計金額
mall_category_sales = pd.pivot_table(data=df,
              index="shopping_mall",
              columns="category",
              values="total_amount",
              aggfunc="sum",
              fill_value=0
              )


# 取引件数
mall_category_count = pd.pivot_table(data=df,
              index="shopping_mall",
              columns="category",
              values="invoice_no",
              aggfunc="count",
              fill_value=0
              )


# ヒートマップによる可視化

figsize = (14, 8)
xlabel = "カテゴリー"
ylabel = "ショッピングモール"
formatter = mtick.FuncFormatter(lambda x, _: f"{int(x):,}")


# 売上合計のヒートマップ
fig,ax = plt.subplots(figsize=figsize, facecolor="white")

# 数値をカンマ付き文字列に変換（同じ形のDataFrameを作る）
annot_df = mall_category_sales.applymap(lambda x: f"{int(x):,}")

sns.heatmap(mall_category_sales,
            annot=annot_df,
            fmt="",
            cmap="YlGnBu",
            linewidth=0.5,
            ax=ax
)

# 見た目調整
colorbar = ax.collections[0].colorbar
colorbar.ax.yaxis.set_major_formatter(formatter)
ax.set_title("モール別 × カテゴリ別の売上合計(TL)(2022年)", fontsize=16)
ax.set_xlabel(xlabel, fontsize=14)
ax.set_ylabel(ylabel, fontsize=14)
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# 出力と保存
plt.tight_layout()
plt.savefig("../output/08_mall_category_sales_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()


# 取引件数のヒートマップ
fig, ax = plt.subplots(figsize=figsize, facecolor="white")

# 数値をカンマ付き文字列に変換（同じ形のDataFrameを作る）
annot_df = mall_category_count.applymap(lambda x: f"{int(x):,}")

sns.heatmap(mall_category_count,
            annot=annot_df,
            fmt="",
           cmap="YlGn",
            linewidths=0.5,
            ax=ax
)

# 見た目調整
colorbar = ax.collections[0].colorbar
colorbar.ax.yaxis.set_major_formatter(formatter)
ax.set_title("モール別 × カテゴリ別の取引件数(2022年)", fontsize =16)
ax.set_xlabel(xlabel, fontsize=14)
ax.set_ylabel(ylabel, fontsize=14)
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# 出力と保存
plt.tight_layout()
plt.savefig("../output/09_mall_category_count_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()
