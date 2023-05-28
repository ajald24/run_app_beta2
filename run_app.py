# 使用するライブラリのインポート
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
import sys ;print(sys.path)

# タイトル
st.title('（※メンテナンス中）ランニングアプリ_街道編')

user_master = pd.read_csv('user_master.csv',encoding='cp932',index_col=['user_name'])

# 新規ユーザの登録
user_input = st.sidebar.selectbox("ユーザID",['新規登録/削除']+[i for i in user_master.index if i!='test'])

if user_input == '新規登録/削除':
    temp_id = st.sidebar.text_input("新規IDを入力してください")
    reg_button =  st.sidebar.button('ユーザ登録')
    del_button = st.sidebar.button('ユーザ削除')
    if reg_button and temp_id not in user_master.index and len(temp_id) != 0:
        user_id = temp_id
        user_master.loc[user_id] = [0,'',0,datetime.today().strftime('%Y/%m/%d'),'',0]
    # ユーザ削除
    elif del_button and len(temp_id) != 0 and temp_id in user_master.index:
        user_master.drop(temp_id,inplace=True) 
        user_id = 'test'
    else: user_id = 'test'
else:
    user_id = user_input

# 街道の指定及び変更
kaido = st.sidebar.selectbox('街道名',("中山道","東海道"))
if user_master.loc[user_id,'course'] == '':
    try:
        user_master.loc[user_id,'course'] = kaido
    except NameError: # デフォルト値の設定
        user_master.loc[user_id,'course'] = '中山道'
    course = user_master.loc[user_id,'course']
else:
    course = user_master.loc[user_id,'course']

if st.sidebar.button('街道変更'):
    user_master.loc[user_id,'course'] = kaido
    user_master.loc[user_id,'course_distance'] = 0

# 走行距離の入力・取消と出力
training_dic = {'ランニング':1,'自転車':0.4,'水泳':4}
training_kind = st.selectbox('運動の種類',['ランニング','自転車','水泳'])
try:
    plus_distance = round(float(st.text_input("今回の走行距離(km)")) * training_dic[training_kind],2)
except ValueError:
    st.write('数値を入力してください')

col1, col2, *cols = st.columns(9)

if col1.button('登録'):
    user_master.loc[user_id,'total_distance'] += plus_distance
    user_master.loc[user_id,'course_distance'] += plus_distance
    user_master.loc[user_id,'last_date'] = datetime.today().strftime('%Y/%m/%d') + f'（↑{plus_distance}km）'
    user_master.loc[user_id,'good'] = 0 # 走行距離登録ごとにいいね数がリセットされる仕様に変更
    
if col2.button('取消'):
    user_master.loc[user_id,'total_distance'] = max(0,user_master.loc[user_id,'total_distance']-plus_distance)
    user_master.loc[user_id,'course_distance'] = max(0,user_master.loc[user_id,'course_distance']-plus_distance)

# # 
feeling_dic = {'😊':0,'🙂':1,'😢':2,'😭':3,'🥱':4,'🤧':5,'✌️':6,'♨️':7,'💔':8,'🐸':9}
feeling_dic2 = {0:'😊',1:'🙂',2:'😢',3:'😭',4:'🥱',5:'🤧',6:'✌️',7:'♨️',8:'💔',9:'🐸'}
today_feeling = st.selectbox('今日の調子は？',feeling_dic.keys())
user_master.loc[user_id,'feeling'] = feeling_dic[today_feeling]

course_distance = user_master.loc[user_id,'course_distance']
total_distance = user_master.loc[user_id,'total_distance']

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
image = Image.open(f'pic/{shukuba}.jpeg')
st.image(image, caption=f'{shukuba}',use_column_width=True)

# いいねするユーザの選択
good_user = st.radio('いいねするユーザ',([i for i in user_master.index if i != 'test']))
# いいねボタン実装
good_button = st.button('👍')
if good_button:
    user_master.loc[good_user,'good'] += 1

# 辞書情報の上書き保存
user_master.to_csv('user_master.csv',encoding='cp932')

st.sidebar.write(f'いいね \n\n{"👍"*int(user_master.loc[user_id,"good"])}')
# # 累計走行距離ランキングの作成
total_ranking = user_master.copy().drop('test').drop(['course','course_distance'],axis=1)
total_ranking.sort_values(by='total_distance',ascending=False,inplace=True)
total_ranking['rank']=range(1,len(total_ranking)+1)
total_ranking=total_ranking.reset_index().set_index('rank')
total_ranking.columns=['ユーザID','累計走行距離(km)','最終更新日（走行距離）','調子','いいね'] # カラム名の設定
total_ranking['いいね']=total_ranking['いいね'].apply(lambda x:'👍'*int(x))
total_ranking['調子']=total_ranking['調子'].map(feeling_dic2)
st.dataframe(total_ranking.head(10)) # 上位10件を表示 

csv = user_master.to_csv().encode('cp932')

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='user_master.csv',
    mime='text/csv',
)
