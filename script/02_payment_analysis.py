import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import japanize_matplotlib
import matplotlib.ticker as mtick


# 2022年のデータを読み込み
df = pd.read_csv("../data/customer_shopping_data_2022.csv")

# 「invoice_date」を日付型に変換
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")


# 決済方法別の売上集計
summary_by_payment = df.groupby("payment_method")["total_amount"].agg(
    total_sales = "sum",
    transaction_count = "count"
).sort_values("total_sales", ascending=False)


# 売上合計の棒グラフ

fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
summary_by_payment["total_sales"].plot(kind="bar", color="#6baed6", ax=ax)

ax.set_title("決済方法別の売上合計(2022年)", fontsize=14)
ax.set_xlabel("決済方法", fontsize=12)
ax.set_ylabel("売上合計(TL)", fontsize=12)

# x軸ラベルを横向きにする
ax.tick_params(axis="x", labelrotation=0)

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

# グラフを描画、画像を保存
plt.tight_layout()
plt.savefig("../output/02_total_sales_by_payment_method.png", dpi=300, bbox_inches="tight")
plt.show()


# 取引件数の棒グラフ

fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
summary_by_payment["transaction_count"].plot(kind="bar", color="#6baed6", ax=ax)

ax.set_title("決済方法別の取引件数(2022年)", fontsize=14)
ax.set_xlabel("決済方法", fontsize=12)
ax.set_ylabel("件数", fontsize=12)

# x軸ラベルを横向きに
ax.tick_params(axis="x", labelrotation=0)

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

# グラフを描画、画像を保存
plt.tight_layout()
plt.savefig("../output/03_transaction_count_by_payment_method.png",
            dpi=300, bbox_inches="tight")
plt.show()
