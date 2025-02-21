#real usersにするかtest usersを含めるかを選択したくなりそうなのでファイルを変えた。realdata_setを書き換えれば良い。
import pandas as pd
import numpy as np
import math
from scipy import stats as st
import matplotlib.pyplot as plt
import os

# Excelファイルを読み込み（file_pathを自分の環境に合わせて変更）
file_path = '/Users/saccyann/Documents/Thinkie/given_file_row/Data_Tracking_20250217.xlsx'
df = pd.read_excel(file_path, sheet_name=2, header=2, index_col=1)
realdata_set = {
    "B2C1", "Trial_Bellettini", "Trial_Fairwinds Brittany Park", "Trial_Empress Senior Living", "Trial_Era Living",
    "Trial_FTJ", "Trial_Murano", "Trial_Solera",
    "Without Sensor", "Woodland Terrace"}

# 1列目の値がrealdata_setに含まれる行のみを抽出
#df = df[df.iloc[:, 1].isin(realdata_set)]
df = df.dropna(subset=[df.columns[1]])

# "IdCount" 列を "Login Id" の右隣に挿入
df.insert(df.columns.get_loc("Login Id") + 1, "IdCount", np.nan)

# LoginIdCount の初期化
LoginIdCount = {}

# 上から順に "Login Id" 列を確認
for index, row in df.iterrows():
    login_id = row["Login Id"]
    
    # LoginIdCount に新しい要素を追加
    if login_id not in LoginIdCount:
        LoginIdCount[login_id] = 1
    else:
        LoginIdCount[login_id] += 1
    
    # "IdCount" 列に記入
    df.at[index, "IdCount"] = LoginIdCount[login_id]

# value が 1 の要素を削除
keys_to_delete = [key for key, value in LoginIdCount.items() if value == 1]

for key in keys_to_delete:
    # 行を削除
    df = df[df["Login Id"] != key]
    # LoginIdCountからも削除
    del LoginIdCount[key]

df = df.reset_index(drop=True)

# value の集合 (set) を取得
value_set = set(LoginIdCount.values())

# brainAgeMeasureFreq の作成
brainAgeMeasureFreq = {value: list(LoginIdCount.values()).count(value) for value in value_set}
listN = []
# keyの抜けを補完してリスト化
for i in range(2,list(brainAgeMeasureFreq.keys())[-1] + 1):
    listN.append(i)
# 正しい辞書
#brainAgeMeasureFreq = {2: 64, 3: 14, 4: 4, 5: 3, 6: 3, 7: 1, 9: 1}
sumnum = sum(brainAgeMeasureFreq.values())
brainAgeMeasureFreq2 = {}
listN =[]
for i in range(2,next(reversed(brainAgeMeasureFreq), None)+1):
    listN.append(i)
#print(listN)
for i in range(1, len(listN)+2):
    brainAgeMeasureFreq2[i]=sumnum
    if i in brainAgeMeasureFreq:
            sumnum -= brainAgeMeasureFreq[i]

#print("brainAgeMeasureFreq2: ", brainAgeMeasureFreq2)

# 対象列
EvaluateItems = ["Brain Age (Avg.)", "Mental Speed Brain Age", "Working Memory Brain Age", "Attention Brain Age"]

# ピボットテーブルの作成
pivot_tables = {}
for item in EvaluateItems:
    pivot_table = df.pivot_table(
        index="IdCount", 
        columns="Login Id", 
        values=item,
        aggfunc='mean'
    )
    pivot_tables[item] = pivot_table
    #print(f"\nPivot Table for {item}:\n", pivot_table)
    pivot_table.index = pivot_table.index.astype(int)
    #print(pivot_table.index)
    #print(type(pivot_tables))

# brainAgeMeasureFreq2 に基づく x の作成
x = []
xnum = 0
for key, freq in brainAgeMeasureFreq2.items():
    x += [key] * freq

# 各ピボットテーブルに対して y を作成して検定を実行
for item, data in pivot_tables.items():
    y = []

    # yの作成
    width = next(iter(brainAgeMeasureFreq2.values())) + 1
    for i in range(len(brainAgeMeasureFreq2)):
        row_data = data.iloc[i, 0:width].tolist()
        y += row_data
    # NaN を除外
    cleaned_y = [z for z in y if not math.isnan(z)]
    #print(len(x))
    #print(x)
    #print(cleaned_y)
    
    # ケンダール検定の実行
    tau, p_value = st.kendalltau(x, cleaned_y)

    print(f"\nKendall's tau for {item}: {tau}")
    print(f"P-value for {item}: {p_value}")

    # p値に基づく解釈
    if p_value < 0.05:
        print("The correlation is statistically significant.")
    else:
        print("The correlation is not statistically significant.")

    for i in range(len(data)-1):
        data.plot(kind='line', stacked=True)
        plt.xlabel('number of trials')
        plt.ylabel('stacked' + item)
        data = data[data.iloc[i+2:, :].columns[data.iloc[i+2:, :].notna().any()].tolist()]
        plt.legend().remove()
        plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/kendall_plot_intestusers/'+item+'_'+str(i)+'.png')
        plt.close() 
