# 使用するライブラリのインポート
import pandas as pd
# import matplotlib.pyplot as plt
import streamlit as st
import pickle
# import folium
# from streamlit_folium import st_folium
from datetime import datetime
from PIL import Image
import sys ;print(sys.path)

# タイトル
st.title('ランニングアプリβ版_街道編')

# 辞書をファイルとして永続化する
# if "st.session_state['users_dic']" not in locals(): # st.session_state['users_dic']の存在確認

# if 'users_dic' not in st.session_state:
#     st.session_state['users_dic'] = {'新規登録/削除':[0,'中山道', 0,'2023/04/09',''],'user_':[0,'中山道', 0,'2023/04/09','','']}
# 後でリセットボタン削除
# if st.sidebar.button('リセット'):
#     st.session_state['users_dic'] = {'新規登録/削除':[0,'中山道', 0,'2023/04/09',''],'user_':[0,'中山道', 0,'2023/04/09','','']}
#     with open("user_dic.pkl","wb") as f:
#         pickle.dump(st.session_state['users_dic'], f)
    # st.session_state['users_dic']["user_"] = [0,'中山道', 0,'2023/04/09',''] # [累計走行距離, 街道, 街道走行距離, 記録開始日付,いいね数]のリスト

# 辞書のインポートと読み込み
with open('user_dic.pkl', 'rb') as f:
    st.session_state['users_dic'] = pickle.load(f)
st.write(st.session_state['users_dic'])

# 新規ユーザの登録
# if st.sidebar.button('新規登録'):
# if  st.session_state['users_dic'].keys() == []:
user_input = st.sidebar.selectbox("ユーザID",[i for i in st.session_state['users_dic'].keys() if i!='user_'])
# else:
#     user_input = st.sidebar.selectbox("ユーザID",['新規登録/削除'])
#     st.session_state['users_dic'] = {'新規登録/削除':[0,'中山道', 0,'2023/04/09',''],'user_':[0,'中山道', 0,'2023/04/09','','']}
if user_input == '新規登録/削除':
    new_id = st.sidebar.text_input("新規IDを入力してください")
    reg_button =  st.sidebar.button('ユーザ登録')
    del_button = st.sidebar.button('ユーザ削除')
    temp_id = 'user_' + new_id
    if reg_button and temp_id not in st.session_state['users_dic'].keys():
        user_id = temp_id
        st.session_state['users_dic'][user_id] = [0,'',0,datetime.today().strftime('%Y/%m/%d'),'','']
    # ユーザ削除
    elif del_button and temp_id != 'user_' and temp_id in st.session_state['users_dic'].keys():
        st.session_state['users_dic'].pop(temp_id) 
        user_id = 'user_'
    else: user_id = 'user_'
else:
    user_id = user_input
# start_date = st.session_state['users_dic'][user_id][3]





# 辞書情報の上書き保存   
with open("st.session_state['users_dic'].pkl","wb") as f:
    pickle.dump(st.session_state['users_dic'], f)

# 街道の指定及び変更
kaido = st.sidebar.selectbox('街道名',("中山道","東海道"))
if st.session_state['users_dic'][user_id][1] == '':
    try:
        st.session_state['users_dic'][user_id][1] = kaido
    except NameError: # デフォルト値の設定
        st.session_state['users_dic'][user_id][1] = '中山道'
    course = st.session_state['users_dic'][user_id][1]
else:
    course = st.session_state['users_dic'][user_id][1]
    # st.markdown('#### 街道名')
    # st.write(course)

if st.sidebar.button('街道変更'):
    # temp_1,temp_2 = st.session_state['users_dic'][user_id][1:3]
    st.session_state['users_dic'][user_id][1] = kaido
    st.session_state['users_dic'][user_id][2] = 0
# if st.sidebar.button('街道変更取消'):
#     st.session_state['users_dic'][user_id][1] = temp_1
#     st.session_state['users_dic'][user_id][2] = temp_2

# 走行距離の入力・取消と出力
try:
    plus_distance = float(st.text_input("今回の走行距離(km)"))
except ValueError:
    st.write('数値を入力してください')

col1, col2, *cols = st.columns(9)

if col1.button('登録'):
    st.session_state['users_dic'][user_id][0] += plus_distance
    st.session_state['users_dic'][user_id][2] += plus_distance
    st.session_state['users_dic'][user_id][3] = datetime.today().strftime('%Y/%m/%d') + f'（↑{plus_distance}km）'
    st.session_state['users_dic'][user_id][4] = '' # 走行距離登録ごとにいいね数がリセットされる仕様に変更
    
if col2.button('取消'):
    st.session_state['users_dic'][user_id][0] = max(0,st.session_state['users_dic'][user_id][0]-plus_distance)
    st.session_state['users_dic'][user_id][2] = max(0,st.session_state['users_dic'][user_id][2]-plus_distance)

# 
today_feeling = st.selectbox('今日の調子は？',['😊','🙂','😢','😭','🥱','🤧','✌️','♨️','💔','🐸'])
st.session_state['users_dic'][user_id][5] = today_feeling[0]

course_distance = st.session_state['users_dic'][user_id][2]
total_distance = st.session_state['users_dic'][user_id][0]
rank_dic = st.session_state['users_dic'].copy()

# ランキング表に不要な情報を削除
rank_dic.pop('新規登録/削除')
# rank_dic = rank_dic.pop('user_01')

# 辞書情報の上書き保存
with open("user_dic.pkl","wb") as f:
    pickle.dump(st.session_state['users_dic'], f)

# 街道名による条件分岐
if course == '中山道':
    temp_list = [[0,10,'日本橋','板橋'],[10,19,'板橋','蕨'],[19,24,'蕨','浦和'],[24,30,'浦和','大宮'],[30,38,'大宮','上尾'],[38,42,'上尾','桶川'],[42,50,'桶川','鴻巣'],[50,66,'鴻巣','熊谷'],[66,78,'熊谷','深谷'],[78,89,'深谷','本庄'],[89,97,'本庄','新町'],[97,104,'新町','倉賀野'],[104,110,'倉賀野','高崎'],[110,117,'高崎','板鼻'],[117,121,'板鼻','安中'],[121,130,'安中','松井田'],[130,139,'松井田','坂本'],[139,150,'坂本','軽井沢'],[150,155,'軽井沢','沓掛'],[155,160,'沓掛','追分'],[160,165,'追分','小田井'],[165,169,'小田井','岩村田'],[169,175,'岩村田','塩名田'],[175,178,'塩名田','八幡'],[178,182,'八幡','望月'],[182,187,'望月','芦田'],[187,192,'芦田','長久保'],[192,200,'長久保','和田'],[200,221,'和田','下諏訪'],[221,233,'下諏訪','塩尻'],[233,239,'塩尻','洗馬'],[239,243,'洗馬','本山'],[243,251,'本山','贄川'],[251,258,'贄川','奈良井'],[258,263,'奈良井','藪原'],[263,271,'藪原','宮ノ越'],[271,279,'宮ノ越','福島'],[279,287,'福島','上松'],[287,300,'上松','須原'],[300,307,'須原','野尻'],[307,316,'野尻','三留野'],[316,321,'三留野','妻籠'],[321,328,'妻籠','馬籠'],[328,333,'馬籠','落合'],[333,337,'落合','中津川'],[337,347,'中津川','大井'],[347,360,'大井','大湫'],[360,367,'大湫','細久手'],[367,378,'細久手','御嵩'],[378,383,'御嵩','伏見'],[383,390,'伏見','太田'],[390,399,'太田','鵜沼'],[399,416,'鵜沼','加納'],[416,422,'加納','河渡'],[422,426,'河渡','美江寺'],[426,435,'美江寺','赤坂'],[435,441,'赤坂','垂井'],[441,446,'垂井','関ヶ原'],[446,450,'関ヶ原','今須'],[450,454,'今須','柏原'],[454,459,'柏原','醒ヶ井'],[459,463,'醒ヶ井','番場'],[463,468,'番場','鳥居本'],[468,474,'鳥居本','高宮'],[474,482,'高宮','愛知川'],[482,492,'愛知川','武佐'],[492,507,'武佐','守山'],[507,513,'守山','草津'],[513,528,'草津','大津'],[528,538,'大津','三条大橋'],[538,course_distance+0.001,'三条大橋','三条大橋']]
elif course == '東海道':
    temp_list = [[0,7.9,'日本橋','品川'],[7.9,17.7,'品川','川崎'],[17.7,27.5,'川崎','神奈川'],[27.5,32.4,'神奈川','保土ヶ谷'],[32.4,41.2,'保土ヶ谷','戸塚'],[41.2,49.1,'戸塚','藤沢'],[49.1,62.8,'藤沢','平塚'],[62.8,65.8,'平塚','大磯'],[65.8,81.5,'大磯','小田原'],[81.5,98.1,'小田原','箱根'],[98.1,112.9,'箱根','三島'],[112.9,118.8,'三島','沼津'],[118.8,124.7,'沼津','原'],[124.7,136.5,'原','吉原'],[136.5,147.7,'吉原','蒲原'],[147.7,151.6,'蒲原','由比'],[151.6,160.8,'由比','興津'],[160.8,164.9,'興津','江尻'],[164.9,175.5,'江尻','府中'],[175.5,181.2,'府中','丸子'],[181.2,189,'丸子','岡部'],[189,195.8,'岡部','藤枝'],[195.8,204.5,'藤枝','島田'],[204.5,208.4,'島田','金谷'],[208.4,215,'金谷','日坂'],[215,222.1,'日坂','掛川'],[222.1,231.7,'掛川','袋井'],[231.7,237.6,'袋井','見附'],[237.6,254,'見附','浜松'],[254,265,'浜松','舞阪'],[265,270.8,'舞阪','新居'],[270.8,277.4,'新居','白須賀'],[277.4,283.2,'白須賀','二川'],[283.2,289.3,'二川','吉田'],[289.3,299.5,'吉田','御油'],[299.5,301.3,'御油','赤坂(東海道)'],[301.3,310.1,'赤坂(東海道)','藤川'],[310.1,316.8,'藤川','岡崎'],[316.8,331.8,'岡崎','池鯉鮒'],[331.8,342.9,'池鯉鮒','鳴海'],[342.9,349.4,'鳴海','宮'],[349.4,376.9,'宮','桑名'],[376.9,389.6,'桑名','四日市'],[389.6,400.4,'四日市','石薬師'],[400.4,403.1,'石薬師','庄野'],[403.1,411,'庄野','亀山'],[411,416.9,'亀山','関'],[416.9,423.4,'関','坂下'],[423.4,433.2,'坂下','土山'],[433.2,443.8,'土山','水口'],[443.8,457.5,'水口','石部'],[457.5,469.3,'石部','草津'],[469.3,483.7,'草津','大津'],[483.7,495.5,'大津','三条大橋'],[495.5,course_distance+0.001,'三条大橋','三条大橋']]
for shuku_list in temp_list:
    if shuku_list[0] <= course_distance < shuku_list[1]:
        shukuba, next_shukuba, rest_distance = [shuku_list[2], shuku_list[3], shuku_list[1]-course_distance]
        break # forループを抜ける
    else:
        continue # skipして次のループへ
if shukuba == '三条大橋':
    st.write('ゴール到着です！\n\nおめでとうございます！！㊗️')
else:
    st.write(f'現在「{shukuba}宿」\n\n 次の宿場「{next_shukuba}宿」まであと{rest_distance:,.2f}km \n\n \t日本橋から{course_distance:,.2f}km')

# 進行割合
total_rate = min(course_distance/temp_list[-1][0],1)
st.sidebar.write(f'累計走行距離{total_distance:,.2f}km')
st.progress(total_rate,text=f'全体の{total_rate*100:,.1f}%')

# 画像の表示
# col1, col2 = st.columns(2)
image = Image.open(f'pic/{shukuba}.jpeg')
st.image(image, caption=f'{shukuba}',use_column_width=True)


# 位置情報の取り込みと地図の表示
pd.options.display.float_format = '{:.0f}'.format # 小数点以下を丸め処理
df_place = pd.read_csv('csv/宿場町.csv',encoding='cp932',index_col=['宿番号']) # 宿場町位置情報の取り込み
st.table(df_place.loc[df_place['宿名']==shukuba,:'旅籠数(軒)'])

# with st.spinner('読み込み中...'):
#     # 地図の中心の緯度/経度、タイル、初期のズームサイズを指定
#     m = folium.Map(
#         # 地図の中心位置の指定
#         location=[df_place.loc[df_place['宿名']==shukuba,'fY'], df_place.loc[df_place['宿名']==shukuba,'fX']], 
#         # タイル、アトリビュートの指定
#         tiles='https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
#         attr='宿場町',
#         # ズームを指定
#         zoom_start=14
#     )

#     # 読み込んだデータ(緯度・経度、ポップアップ用文字、アイコンを表示)
#     for i, row in df_place.iterrows():
#         # ポップアップの作成(宿名＋住所)
#         pop=f"{row['宿名']}({row['現・住所']})"
#         folium.Marker(
#             # 緯度と経度を指定
#             location=[row['fY'], row['fX']],
#             # ツールチップの指定(都道府県名)
#             tooltip=row['宿名'],
#             # ポップアップの指定
#             popup=folium.Popup(pop, max_width=300),
#             # アイコンの指定(アイコン、色)
#             icon=folium.Icon(icon="home",icon_color="white", color="red")
#         ).add_to(m)
    
#     # with col2:
# st_data = st_folium(m, width=350, height=300)

# st.success('反映完了！')

# いいねするユーザの選択
good_user = st.radio('いいねするユーザ',([i for i in rank_dic.keys() if i != 'user_']))
# いいねボタン実装
good_button = st.button('👍')
if good_button:
    rank_dic[good_user][4] += '👍'
    # 辞書情報の上書き保存
    with open("user_dic.pkl","wb") as f:
        pickle.dump(st.session_state['users_dic'], f)
# 毎週月曜日の0時0分0秒にいいね数をリセット
# if datetime.now().strftime('%A/%H:%M:%S')=='Monday/00:00:00':
# #     for user in rank_dic.keys():
#         rank_dic[user][4] = ''  
    # 辞書情報の上書き保存
    # with open("st.session_state['users_dic'].pkl","wb") as f:
    #     pickle.dump(st.session_state['users_dic'], f)  

st.sidebar.write(f'いいね \n\n{rank_dic[user_id][4]}')
# 累計走行距離ランキングの作成
total_ranking = pd.DataFrame(rank_dic).T # 転置
total_ranking.reset_index(inplace=True) # indexのリセット
total_ranking.columns=['ユーザID','累計走行距離(km)','街道','街道走行距離(km)','最終更新日（走行距離）','いいね','調子'] # カラム名の設定
# total_ranking['いいね']=''
total_ranking = total_ranking.loc[total_ranking['ユーザID']!='user_',['ユーザID','累計走行距離(km)','最終更新日（走行距離）','調子','いいね']]
total_ranking.sort_values('累計走行距離(km)',ascending=False,inplace=True) # 累計走行距離が長い順に並べ替え
total_ranking.index=total_ranking['累計走行距離(km)'].rank(ascending=False,method='min').astype(int) # ランキング(降順)の付与
st.subheader('走行距離ランキング') # タイトル
st.dataframe(total_ranking.head(10)) # 上位10件を表示 
# fig,ax = plt.subplots(figsize=(10,5))
# ax.bar(total_ranking.index,total_ranking['累計走行距離'])
# st.pyplot(fig)

if st.sidebar.text_input('') == 'run_app_beta2_reset':
    st.session_state['users_dic'] = {'新規登録/削除':[0,'中山道', 0,'2023/04/09',''],'user_':[0,'中山道', 0,'2023/04/09','','']}
    with open("user_dic.pkl","wb") as f:
        pickle.dump(st.session_state['users_dic'], f)

