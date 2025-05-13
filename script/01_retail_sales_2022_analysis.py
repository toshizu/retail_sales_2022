import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import japanize_matplotlib
import matplotlib.ticker as mtick


df = pd.read_csv("../data/customer_shopping_data.csv")


# 「invoice_date」を日付型に変換
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")


# 2022年を抽出
df_2022 = df[df["invoice_date"].dt.year == 2022].copy()

# 売り上げ金額の列を追加
df_2022["total_amount"] = df_2022["price"] * df_2022["quantity"]


# 年齢を10で区切ったデータの列を新たに追加
df_2022["age_group"] = (df_2022["age"] // 10 * 10).astype(str) + "s"


# 性別・年代別の売上集計
gender_age_sales = df_2022.groupby(["gender", "age_group"])["total_amount"].sum().unstack()


# 2022年のみ抽出したデータフレームをcsvファイルで保存
df_2022.to_csv("../data/customer_shopping_data_2022.csv", index=False)


# 棒グラフによる可視化

# カラー設定
colors = {
    "Female": "#f7c6c7", #ベビーピンク
    "Male": "#6ca0dc"    #スカイブルー
}

# 色純を性別の列順に合わせる
color_list = [colors[gender] for gender in gender_age_sales.index]


fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
gender_age_sales.T.plot(kind="bar", ax=ax, color=color_list)

# タイトル・軸ラベル
ax.set_title("性別×年代別の売上集計(2022年)", fontsize=14)
ax.set_xlabel("年代", fontsize=12)
ax.set_ylabel("売上合計(TL)", fontsize=12)

# Y軸をカンマ区切りに
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

ax.tick_params(axis="x", rotation=0)

# 凡例の日本語ラベル定義
japanese_labels = ["女性", "男性"]
#凡例を上書き
ax.legend(labels=japanese_labels, title="性別")

# グラフ画像を保存して描画
plt.tight_layout()
plt.savefig("../output/01_gender_age_sales_2022.png", dpi=300, bbox_inches="tight")
plt.show()
