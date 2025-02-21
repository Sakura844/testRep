'''
関数はdfを受け取る形にし、実行時にreal_datasetの行を抽出する形に統一
・3行目から（２行ぶん空欄）B列開始で以下の順番に格納する。
No	Community	Login Id	Data Tracking No	Data Tracking Name	Training Name	Thinkie Point	Training Score	Brain Age Check Name	Data Tracking Date And Time
・もらったexcelファイルは日付で昇順に直す
・realdata_setにreal dataのcommunityをすべて追加していることを確認する
・file_pathはすべて書き換える
'''
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter
from datetime import datetime, timedelta

# Excelファイルを読み込む
file_path = '/Users/saccyann/Documents/Thinkie/given_file_row/Data_Tracking_20250217.xlsx'

def wearingRate(df, title):
    # 6列目が0である行と0でない行をカウント
    zero_count = len(df[df.iloc[:, 6] == "0"])
    non_zero_count = len(df[(df.iloc[:, 6] != "0") & (df.iloc[:, 6] != "none")])

    # 結果を表示
    print(f"{title} - Not Wearing: {zero_count}")
    print(f"{title} - Wearing: {non_zero_count}")

    # 割合を計算
    total_count = zero_count + non_zero_count
    zero_percentage = (zero_count / total_count) * 100
    non_zero_percentage = (non_zero_count / total_count) * 100

    # 円グラフを作成
    labels = ['Not Wearing', 'Wearing']
    sizes = [zero_percentage, non_zero_percentage]
    colors = ['lightcoral', 'lightgreen']
    explode = (0.1, 0)  # 'Zero'部分を少し突出させる

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title(f"Percentage of users wearing a brain meter ({title})")
    plt.axis('equal')  # 円を丸く保つ
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/wearingRate_'+title+'.png')
    
def daysSinceLastBrainage(df, title):
    # DataFrameのうちbrainageをチェックして有限の値だった行を取得
    df = df[(df.iloc[:, 4] == "BRAIN_AGE_CHECK_END") & (df.iloc[:, 8] != "none")]

    # 9列目の日時をリストに格納する（時刻を無視）
    days_diff_list = []

    # dfの9列目をループ
    for _, row in df.iterrows():
        # 9列目の日付を取得
        brain_meter_last_date = pd.to_datetime(row.iloc[9]) 
        
        # 日付差を計算（時刻を無視して日数）
        days_diff = (last_date - brain_meter_last_date).days
        
        # 結果をリストに格納
        days_diff_list.append(abs(days_diff))  # 絶対値を取っておく
    # **df用のヒストグラム**
    plt.figure(figsize=(10, 6))
    plt.hist(days_diff_list, bins=20, color='orange', edgecolor='black')
    plt.title(title)
    plt.xlabel('Days elapsed since last brain age measurement')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/daysSinceLastBrainage_'+title+'.png')
    
def daysSinceLastGame(df, title):
    # 'TRAINING_END' の行を抽出
    training_end_data = df[df.iloc[:, 4] == 'TRAINING_END']

    # 辞書を作成
    training_end_dict = {}
    for _, row in training_end_data[::-1].iterrows():  # 末尾から順番に探索
        key = row.iloc[2]  # 2列目の値をキーに
        value_str = row.iloc[9]  # 9列目の日付文字列を取得

        # "none" や不正な値があればスキップ
        if value_str == "none" or pd.isna(value_str):
            continue

        try:
            value = pd.to_datetime(value_str)  # 日付型に変換
        except Exception as e:
            print(f"日付変換エラー: {value_str} - {e}")
            continue  # エラーがあった場合はスキップ

        if key not in training_end_dict:
            training_end_dict[key] = value

    # 辞書の各値（value）に対して、'last_date' との日数差を計算
    days_diff = []
    for value in training_end_dict.values():
        # 'last_date'との差を計算（時刻は無視）
        days = (last_date - value).days
        days_diff.append(days)
        
    # **df用のヒストグラム**
    plt.figure(figsize=(10, 6))
    plt.hist(days_diff, bins=20, color='orange', edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel('Days Since Last Training End')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/daysSinceLastGame_'+title+'.png')

def freeUserGamePlay(df, title):
    # 空の辞書を作成
    user_count = {}

    # DataFrame の全行をループ処理
    for _, row in df.iterrows():
        user_id = row.iloc[1]  # 1列目の userID を取得

        # userID が辞書に存在しなければ初期化
        if user_id not in user_count:
            user_count[user_id] = 0

        # 出現回数をカウント
        user_count[user_id] += 1

    # 出現回数を降順でソートし、上位10人を取得
    top_10_users = sorted(user_count.items(), key=lambda x: x[1], reverse=True)[:10]

    # 結果を出力
    print(f"\nTop 10 Users by Appearance Count in {title}:")
    for user, count in top_10_users:
        print(f"{user}: {count} times")
        
    # dfのヒストグラム
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)  # 1行2列、1番目の位置にヒストグラムを描画
    plt.hist(user_count.values(), bins=20, edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/freeUserGamePlay_'+title+'.png')

def constantUsers(df,title):
    #(0)初回loginから1ヶ月経過後以降にもloginしたuserの集合と総数
    constant_users = set()
    login_data = df[df.iloc[:, 4] == "LOGIN"]
    user_expiry_dict = {}
    for _, row in login_data.iterrows():
        key = row.iloc[2]  # 2列目の値（ユーザーID）
        value = row.iloc[9] + timedelta(days=30)  # 9列目の日付 +1ヶ月
        if key not in user_expiry_dict:
            user_expiry_dict[key] = value

    for key, expiry_date in user_expiry_dict.items():
        matching_rows = df[(df.iloc[:, 9] >= expiry_date) & (df.iloc[:, 2] == key) & (df.iloc[:, 4] == "LOGIN")]
        if not matching_rows.empty:
            constant_users.add(key)

    print("Constant Users:", constant_users)
    print("Total Count of Constant Users:", len(constant_users))

def loginPerCommunity(df, last_date):
    #生きてるB2Bコミュニティを抽出
    selected_data_set = {"Trial_Bellettini", "Trial_Fairwinds Brittany Park", "Trial_Empress Senior Living", "Trial_FTJ"}
    # 1列目の値がselected_data_setに含まれる行のみを抽出
    df_b2b = df[df.iloc[:, 1].isin(selected_data_set)]
    df_b2b = df_b2b.reset_index(drop=True)
    
    # B2C1 のみを抽出
    df_b2c1 = df[df.iloc[:, 1] == "B2C1"]
    df_b2c1 = df_b2c1.reset_index(drop=True)

    # 最新の日曜日を計算
    days_diff = (last_date.weekday() + 1) % 7  # 0: 月曜日, 6: 日曜日
    latest_sunday = last_date - pd.Timedelta(days=days_diff)

    # B2B の辞書
    community_dict = {user: {} for user in selected_data_set}
    community_dict_4weeks = {user: {} for user in selected_data_set}
    
    # B2C1 の辞書
    b2c1_dict = {"B2C1": {}}
    b2c1_dict_4weeks = {"B2C1": {}}

    # 直近の日曜日から7日ごとに繰り返し処理
    for i in range(0, 30):  # 30週間分
        start_date = latest_sunday - pd.Timedelta(days=i * 7)
        end_date = start_date + pd.Timedelta(days=6)  # 7日間

        # B2B の処理
        mask_b2b = (df_b2b.iloc[:, 9] >= start_date) & (df_b2b.iloc[:, 9] <= end_date) & (df_b2b.iloc[:, 4] == "LOGIN")
        filtered_df_b2b = df_b2b[mask_b2b]

        for community in selected_data_set:
            loginN = filtered_df_b2b[filtered_df_b2b.iloc[:, 1] == community].shape[0]
            community_dict[community][start_date.strftime('%Y-%m-%d')] = loginN

            if i < 4:  # 4週間分
                community_dict_4weeks[community][start_date.strftime('%Y-%m-%d')] = loginN

        # B2C1 の処理
        mask_b2c1 = (df_b2c1.iloc[:, 9] >= start_date) & (df_b2c1.iloc[:, 9] <= end_date) & (df_b2c1.iloc[:, 4] == "LOGIN")
        filtered_df_b2c1 = df_b2c1[mask_b2c1]

        b2c1_dict["B2C1"][start_date.strftime('%Y-%m-%d')] = filtered_df_b2c1.shape[0]
        if i < 4:
            b2c1_dict_4weeks["B2C1"][start_date.strftime('%Y-%m-%d')] = filtered_df_b2c1.shape[0]
                
    # B2B グラフ
    B2BFlags = [[community_dict_4weeks, "B2B 4 weeks"], [community_dict, "B2B 30 weeks"]]
    for i in range(2):
        plt.figure(figsize=(12, 6))
        colors2 = plt.colormaps.get_cmap('tab10', len(selected_data_set))

        for idx, (community, data) in enumerate(B2BFlags[i][0].items()):
            dates = list(data.keys())
            login_counts = list(data.values())
            plt.plot(dates[::-1], login_counts[::-1], label=community, color=colors2(idx))

        plt.title(B2BFlags[i][1])
        plt.xlabel('Date')
        plt.ylabel('Login Count')
        plt.xticks(rotation=45)
        plt.legend(title="Community", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/loginPerCommunity_B2B_'+str(i)+'.png')

    # B2C1 グラフ
    B2C1Flags = [[b2c1_dict_4weeks, "B2C1 4 weeks"], [b2c1_dict, "B2C1 30 weeks"]]
    for i in range(2):
        plt.figure(figsize=(12, 6))
        colors_b2c1 = plt.colormaps.get_cmap('tab10', 1)

        for idx, (community, data) in enumerate(B2C1Flags[i][0].items()):
            dates = list(data.keys())
            login_counts = list(data.values())
            plt.plot(dates[::-1], login_counts[::-1], label=community, color=colors_b2c1(idx))

        plt.title(B2C1Flags[i][1])
        plt.xlabel('Date')
        plt.ylabel('Login Count')
        plt.xticks(rotation=45)
        plt.legend(title="B2C", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout() 
        plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/loginPerCommunity_B2C_'+str(i)+'.png')
        
def findPowerUsers(names_tab3):
    # 複数回登場する名前を set で取得
    name_counts = Counter(names_tab3)
    Users_Measured_BrainAge_MultiTimes_List = {name for name, count in name_counts.items() if count > 1}

    # 辞書を作成（初期値 0）
    Users_Measured_BrainAge_MultiTimes = {name: 0 for name in Users_Measured_BrainAge_MultiTimes_List}

    # TRAINING_END の行の D列を取得
    filtered_names = df_tab2.loc[df_tab2['Data Tracking Name'] == 'TRAINING_END', 'Login Id'].dropna()

    # カウントを増やす
    for name in filtered_names:
        if name in Users_Measured_BrainAge_MultiTimes:
            Users_Measured_BrainAge_MultiTimes[name] += 1

    # チェック
    #print("Users_Measured_BrainAge_MultiTimes_List:", Users_Measured_BrainAge_MultiTimes_List)
    #print(Users_Measured_BrainAge_MultiTimes)

    '''以下は2回以上Brain Ageを測定したUsersのゲームプレイ回数の統計。気になった時だけやればいい
    # 辞書の value のみをリストに変換
    values = list(Users_Measured_BrainAge_MultiTimes.values())

    # 平均値の計算
    mean_value = np.mean(values)

    # 四分位数の計算
    quartiles = np.percentile(values, [25, 50, 75])

    # 結果を表示
    print("Mean:", mean_value)
    print("Quartile:")
    print("  First Quartile (25%):", quartiles[0])
    print("  Second Quartile (Median, 50%):", quartiles[1])
    print("  Third Quartile (75%):", quartiles[2])
    '''
    # value が 30 以上の key を取得
    keys_with_value_30_or_more = [key for key, value in Users_Measured_BrainAge_MultiTimes.items() if value >= 30]

    # 結果を表示
    #print("List of users who have measured Brain Age at least twice and have played the game at least 30 times:")
    #print(keys_with_value_30_or_more)
    print(len(keys_with_value_30_or_more))

def gamePlayTime(file_path, df, title):
    realdata_set = {
        "B2C1", "Trial_Bellettini", "Trial_Fairwinds Brittany Park", "Trial_Empress Senior Living", "Trial_Era Living",
        "Trial_FTJ", "Trial_Murano", "Trial_Solera",
        "Without Sensor", "Woodland Terrace"}

    # 1列目の値がrealdata_setに含まれる行のみを抽出
    #df = df[df.iloc[:, 1].isin(realdata_set) & ((df.iloc[:, 4] == "TRAINING_END") | (df.iloc[:, 4] == "TRAINING_START"))]
    df = df[df.iloc[:, 1].isin(realdata_set)]
    df = df.reset_index(drop=True)

    # "TRAINING_END" の行をフィルタリング
    training_end_rows = df[df.iloc[:, 4] == "TRAINING_END"]

    # 結果を格納するリスト
    date_diff_list = []

    # "TRAINING_END"行ごとに処理
    for idx, row in training_end_rows.iterrows():
        # 現在の行の2列目（キー）と9列目（TRAINING_ENDの日時）
        key = row.iloc[2]
        training_end_date = pd.to_datetime(row.iloc[9])

        # 直前の行から遡って
        for previous_idx in range(idx-1, -1, -1):
            previous_row = df.iloc[previous_idx]
            
            # 同じキーで、かつ"TRAINING_START"の行を見つける
            if previous_row.iloc[2] == key and previous_row.iloc[4] == "TRAINING_START":
                training_start_date = pd.to_datetime(previous_row.iloc[9])
                
                # 日付の差を計算
                date_diff = abs((training_end_date - training_start_date).total_seconds())
                date_diff_list.append(date_diff)
                break  # 見つかったら次の"TRAINING_END"行に進む
            
    # 最大値2つを外れ値として削除
    date_diff_list.remove(max(date_diff_list))  
    date_diff_list.remove(max(date_diff_list))    

    top_10 = sorted(date_diff_list, reverse=True)[:10]
    print("10 Longest Playing Tim (sec): ", top_10)

    mean = np.mean(date_diff_list)  # 平均値
    max_value = np.max(date_diff_list)  # 最大値
    min_value = np.min(date_diff_list)  # 最小値
    q1 = np.percentile(date_diff_list, 25)  # 第1四分位数(Q1)
    q2 = np.median(date_diff_list)  # 第2四分位数(Q2, 中央値)
    q3 = np.percentile(date_diff_list, 75)  # 第3四分位数(Q3)

    print(f"Mean: {mean}")
    print(f"Max: {max_value}")
    print(f"Min: {min_value}")
    print(f"Q1 (First Quartile): {q1}")
    print(f"Q2 (Median): {q2}")
    print(f"Q3 (Third Quartile): {q3}")
    
    # **ヒストグラム**
    plt.figure(figsize=(10, 6))
    plt.hist(date_diff_list, bins=20, color='orange', edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel('Game Time Seconds')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/gameplaytime_'+title+'.png')
    
def longtermUsersAnalysis(df, title):
    # 長期userを定義
    long_thre = last_date - timedelta(days=150)
    # "Data Tracking Name" 列が "LOGIN" の行を抽出
    dfLogin = df[df["Data Tracking Name"] == "LOGIN"]

    # "Data Tracking Date And Time" 列の日付を datetime 型に変換
    #dfLogin["Data Tracking Date And Time"] = pd.to_datetime(dfLogin["Data Tracking Date And Time"])
    # long_thre 以前の "Login Id" を持つ行を抽出
    dfOldLogin = dfLogin[dfLogin["Data Tracking Date And Time"] <= long_thre]
    dfRecentLogin = dfLogin[dfLogin["Data Tracking Date And Time"] > long_thre]
    
    # 長期・短期ユーザーの集合を作成
    long_term_users = set(dfOldLogin["Login Id"].unique())
    short_term_users = set(dfRecentLogin["Login Id"].unique())

    # 月ごとに遡ってカウント
    date_range = pd.date_range(end=last_date, periods=12, freq='ME')
    long_term_login_counts = []
    other_login_counts = []

    for i in range(len(date_range)-1):
        start_date = date_range[i]
        end_date = date_range[i+1]
        df_month = dfLogin[(dfLogin["Data Tracking Date And Time"] > start_date) & (dfLogin["Data Tracking Date And Time"] <= end_date)]
        
        # long_term_users に含まれるユーザーのログイン数
        long_term_count = df_month[df_month["Login Id"].isin(long_term_users)].shape[0]
        long_term_login_counts.append(long_term_count)
        
        # その他のユーザーのログイン数
        other_count = df_month[~df_month["Login Id"].isin(long_term_users)].shape[0]
        other_login_counts.append(other_count)

    # 月のラベルを作成
    months = [date.strftime('%Y-%m') for date in date_range[:-1]]

    # グラフの描画
    plt.figure(figsize=(10, 6))
    plt.plot(months, long_term_login_counts, label='Long Term Users - '+str(len(long_term_users)), marker='o')
    plt.plot(months, other_login_counts, label='Short Term Users - '+str(len(short_term_users)), marker='o')
    plt.xlabel('Month')
    plt.ylabel('Login Count')
    plt.title('Monthly Login Count Comparison (thresh = 150 days) '+title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # グラフの保存
    output_path = '/Users/saccyann/Documents/Thinkie/Data_Visualization_Code2_'+title+'.png'
    plt.savefig(output_path)

def longtermUsersAnalysis(df, title):
    # 長期userを定義
    long_thre = last_date - timedelta(days=150)
    # "Data Tracking Name" 列が "LOGIN" の行を抽出
    dfLogin = df[df["Data Tracking Name"] == "LOGIN"]
    #print(dfLogin.shape)
    
    # "Data Tracking Date And Time" 列の日付を datetime 型に変換
    #dfLogin["Data Tracking Date And Time"] = pd.to_datetime(dfLogin["Data Tracking Date And Time"])
    # long_thre 以前の "Login Id" を持つ行を抽出
    dfOldLogin = dfLogin[dfLogin["Data Tracking Date And Time"] <= long_thre]
    dfRecentLogin = dfLogin[dfLogin["Data Tracking Date And Time"] > long_thre]
    #print(dfOldLogin.shape)
    #print(dfRecentLogin.shape)
    
    # 長期・短期ユーザーの集合を作成
    long_term_users = set(dfOldLogin["Login Id"])
    short_term_users = set(dfRecentLogin["Login Id"])
    # 月ごとに遡ってカウント
    # last_dateの前月も含めるように修正
    date_range = pd.date_range(end=last_date, periods=13, freq='M')
    
    # 'for' ループでの月ごとの処理修正
    long_term_login_counts = []
    other_login_counts = []
    long_term_gameplay_counts = []
    other_gameplay_counts = []

    for i in range(len(date_range)-1):
        # start_dateとend_dateを修正
        start_date = date_range[i]
        end_date = date_range[i+1] - timedelta(days=1)  # end_dateを前日のみに修正
        
        # 修正：月ごとのデータ抽出
        df_month = dfLogin[(dfLogin["Data Tracking Date And Time"] > start_date) & (dfLogin["Data Tracking Date And Time"] <= end_date)]
        df_month_gameplay = df[(df["Data Tracking Name"] == "TRAINING_END") & (df["Data Tracking Date And Time"] > start_date) & (df["Data Tracking Date And Time"] <= end_date)]
        
        # long_term_users に含まれるユーザーのログイン数
        long_term_count = df_month[df_month["Login Id"].isin(long_term_users)].shape[0]
        long_term_login_counts.append(long_term_count)
        
        # その他のユーザーのログイン数
        other_count = df_month[~df_month["Login Id"].isin(long_term_users)].shape[0]
        other_login_counts.append(other_count)
        
        # long_term_users に含まれるユーザーのゲーム数
        long_term_gameplay_count = df_month_gameplay[df_month_gameplay["Login Id"].isin(long_term_users)].shape[0]
        long_term_gameplay_counts.append(long_term_gameplay_count)
        
        # その他のユーザーのゲーム数
        other_gameplay_count = df_month[~df_month["Login Id"].isin(long_term_users)].shape[0]
        other_gameplay_counts.append(other_gameplay_count)

    # 月のラベルを作成
    months = [date.strftime('%Y-%m') for date in date_range[:-1]]
    months = [(pd.to_datetime(month) + pd.DateOffset(months=1)).strftime('%Y-%m') for month in months]
    
    # グラフの描画
    plt.figure(figsize=(10, 6))
    plt.plot(months, long_term_login_counts, label='Long Term Users - '+str(len(long_term_users)), marker='o')
    plt.plot(months, other_login_counts, label='Short Term Users - '+str(len(short_term_users)), marker='o')
    plt.xlabel('Month')
    plt.ylabel('Login Count')
    plt.title('Monthly Login Count (thresh = 150 days) '+title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/Data_tracking_plot/Data_Visualization_Code2_Login_'+title+'.png')
    
    # グラフの描画_ゲーム数
    plt.figure(figsize=(10, 6))
    plt.plot(months, long_term_gameplay_counts, label='Long Term Users - '+str(len(long_term_users)), marker='o')
    plt.plot(months, other_gameplay_counts, label='Short Term Users - '+str(len(short_term_users)), marker='o')
    plt.xlabel('Month')
    plt.ylabel('Training End Count')
    plt.title('Monthly Training End Count (thresh = 150 days) '+title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code2_Training_End_'+title+'.png')


def reloginTrend(df):
    # (0) 初期設定
    days_list = [10, 20, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365]
    relogin_counts = []   # 再ログイン人数を格納
    initial_counts = []   # 30, 50, 100, ... 日以前に初回ログインしている人数を格納
    
    # (1) 基準日を設定（データの最終行の日付）
    last_date = pd.to_datetime(df.iloc[-1, 9])
    
    # (2) ユーザーごとの初回ログイン日を取得
    user_first_login_dict = {}
    login_data = df[df.iloc[:, 4] == "LOGIN"]
    for _, row in login_data.iterrows():
        user_id = row.iloc[2]  # ユーザーID
        login_date = row.iloc[9]  # ログイン日
        
        # 初めて見たユーザーIDなら、初回ログイン日を記録
        if user_id not in user_first_login_dict:
            user_first_login_dict[user_id] = login_date
    
    # (3) 50, 100, ..., 300 日前以前に初回ログインを終えた人数をカウント
    for days in days_list:
        cutoff_date = last_date - timedelta(days=days)
        initial_count = sum(1 for date in user_first_login_dict.values() if date <= cutoff_date)
        initial_counts.append(initial_count)
    
    # (4) 再ログイン人数のカウント
    for days in days_list:
        constant_users = set()
        for user_id, first_login in user_first_login_dict.items():
            expiry_date = first_login + timedelta(days=days)
            
            # expiry_date 以降に再ログインしているか確認
            matching_rows = df[
                (df.iloc[:, 9] >= expiry_date) &  # 日付が expiry_date 以降
                (df.iloc[:, 2] == user_id) &     # ユーザーIDが一致
                (df.iloc[:, 4] == "LOGIN")       # イベントが LOGIN
            ]
            
            # 再ログインしているなら、constant_users に追加
            if not matching_rows.empty:
                constant_users.add(user_id)
        
        # 再ログイン人数をリストに追加
        relogin_counts.append(len(constant_users))
        relogin_rate = [round((re / init) * 100, 2) for re, init in zip(relogin_counts, initial_counts)]
        
        retention_list = [ str(day) + " days after the first login: " + str(rate) + " % (" + str(relogin) + " out of " + str(firstlogin) +")"  for day, rate, relogin, firstlogin in zip(days_list, relogin_rate, relogin_counts, initial_counts)]
    
    # (5) 結果の表示
    #print(f"日数リスト: {days_list}")
    #print(f"初回ログイン人数: {initial_counts}")
    #print(f"再ログイン人数: {relogin_counts}")
    #print(f"再ログイン割合: {relogin_rate}")
    for i in retention_list:
        print(i)
    
    # 折れ線グラフを描画
    plt.plot(days_list, relogin_rate, marker='o', linestyle='-', color='blue', label='Relogin Rate')
    # 軸ラベル、タイトル、凡例の設定
    plt.xlabel('Days')
    plt.title('Re-login Rate Over Time (%)')
    plt.legend()
    # y軸の最小値を0に設定
    plt.ylim(bottom=0)
    # グラフの表示
    plt.grid(True)
    plt.savefig('/Users/saccyann/Documents/Thinkie/Data_Visualization_Code/relogin_rate_over_time.png')
    
# dfを読み込む
df = pd.read_excel(file_path, sheet_name=1, header=2, index_col=1)
realdata_set = {
    "B2C1", "Trial_Bellettini", "Trial_Fairwinds Brittany Park", "Trial_Empress Senior Living", "Trial_Era Living",
    "Trial_FTJ", "Trial_Murano", "Trial_Solera",
    "Without Sensor", "Woodland Terrace"}

# 1列目の値がrealdata_setに含まれる行のみを抽出
df = df[df.iloc[:, 1].isin(realdata_set)]
df = df.reset_index(drop=True)

# "B2C1" の行だけを抽出
dfb2c = df[df.iloc[:, 1] == "B2C1"]
# training_endを抽出
dfTE = df[df.iloc[:, 4] == "TRAINING_END"]
# dfb2cを作成
dfb2cTE = dfTE[(dfTE.iloc[:, 1] == "B2C1") & (dfTE.iloc[:, 4] == "TRAINING_END")]

# 最新の日付を取得（dfの最後の行の9列目）
last_date = pd.to_datetime(df.iloc[-1, 9])


#7 - Login Per Community
loginPerCommunity(df, last_date)

#6 - loginGameendTrend - long term users vs short term users
longtermUsersAnalysis(df, "All_Users")
longtermUsersAnalysis(dfb2c, "B2C_Users")

#3 - daysSinceLastGame
daysSinceLastGame(df, 'All Users')
daysSinceLastGame(dfb2c, 'B2C Users')

#2 - Days Since Last Brain Age関数
daysSinceLastBrainage(df, 'All Users')
daysSinceLastBrainage(dfb2c, 'B2C Users')


#5 - gamePlayLength
gamePlayTime(file_path, df, "All users")
gamePlayTime(file_path, dfb2c, "B2C users")

#1 - wearingRate
wearingRate(dfTE, "df")
wearingRate(dfb2cTE, "dfb2c")

#4 - Free Users Game Count & Brain Age Count
# ファイルを読み込む。sheet_nameは2025/2/4時点で5枚目が無料版userのゲーム履歴だったので5。
dfF = pd.read_excel(file_path, sheet_name=3, header=2, index_col=1)
dfFTE = dfF[dfF.iloc[:, 4] == "TRAINING_END"]
dfFBA = dfF[dfF.iloc[:, 4] == "BRAIN_AGE_CHECK_END"]
freeUserGamePlay(dfFTE, 'GamePlay')
freeUserGamePlay(dfFBA, 'Brain Age Measurement')

#8 - Login/Gameplay/Game preference/Constant users
constantUsers(df, "All Users")
constantUsers(dfb2c, "B2C")

#9 - Find Power Users
# 3つ目のタブを読み込む（D列）
df_tab3 = pd.read_excel(file_path, sheet_name=2, header=2, index_col=1)
names_tab3 = df_tab3['Login Id'].dropna()
# 2つ目のタブを読み込む
df_tab2 = pd.read_excel(file_path, sheet_name=1, header=2, index_col=1)
findPowerUsers(names_tab3)

#10 - reloginTrend(df)
reloginTrend(df)

# 最後にplt.show()でグラフを表示
#plt.show()
