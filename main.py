import pandas as pd
import glob
import os  # ✅ 添加此模块用于创建目录

# 第一步：读取所有 CSV 文件
all_files = glob.glob("data/*.csv")
df_list = [pd.read_csv(f) for f in all_files]
df = pd.concat(df_list, ignore_index=True)

# 第二步：筛选只保留 pink morsel
df = df[df["product"].str.lower() == "pink morsel"]

# 第三步：转换价格格式，计算销售额
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["price"] * df["quantity"]

# 第四步：提取所需字段
final_df = df[["sales", "date", "region"]]

# ✅ 新增：确保输出文件夹存在
os.makedirs("output", exist_ok=True)

# 第五步：保存文件
final_df.to_csv("output/cleaned_sales.csv", index=False)

print("✅ 成功生成 cleaned_sales.csv！")
