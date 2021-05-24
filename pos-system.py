import datetime
import pandas as pd

###　商品クラス
class Item:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def get_price(self):
        return self.price

    def get_name(self):
        return self.item_name

### オーダークラス
class Order:
    def __init__(self, item_master):
        self.item_order_list = []
        self.item_master = item_master
    
    def add_item_order(self, item_ordered):
        self.item_order_list.append(item_ordered)
    
    def order_list(self):
    #オーダーリストをDFに格納
        df = pd.DataFrame()
        df['code'] = [item.split()[0] for item in self.item_order_list]
        df['qty'] = [int(item.split()[1]) for item in self.item_order_list]
        return df

    def view_item_list(self, master):
    # オーダーの一覧を表示
        lists = self.order_list()
        for i in lists.index:
            code = lists.iloc[i]['code']
            name = master.loc[code]['商品名']
            price = master.loc[code]['価格']
            qty = lists.iloc[i]['qty']
            print('商品コード：{} 商品名：{} 価格：{:,}円  ×　{}個'.format(code, name, price, qty))

    def view_order_summary(self, master):
    #オーダー一覧をグループ化して表示
        summary = self.order_list().groupby('code')
        for code, group in summary:
            name = master.loc[code]['商品名']
            price = master.loc[code]['価格']
            print('{}({:,}円): {:,}個'.format(name, price, group.sum()['qty']))
            
        return summary

    def calc_order_ttl(self, master, order_summary):
        ttl = 0
        for code, group in order_summary:
            price = master.loc[code]['価格']
            ttl = ttl + group.sum()['qty'] * price
        print('合計金額は{:,}円になります。'.format(ttl)) 
        return ttl

    def calc_payment(self, ttl):
        payment = ''
        
        while payment != 'done':
            print('受け取った代金を入力してください。')
            money = int(input())
            exchange = money - ttl

            if money == ttl:
                print('ありがとうございました。ちょうどお預かりします。')
                payment = 'done'
            elif money > ttl:
                print('ありがとうございました。{:,}円のお返しです。'.format(exchange))
                payment = 'done'
            else:
                print('お代が足りません。')
            return money, exchange

    def receipt(self, master, money, exchange):
    # レシートを出力
        with open('receipt.txt', 'w', encoding='UTF-8') as f:
            #日付
            dt_now = datetime.datetime.now()
            f.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
            
            #オーダー一覧を書き出し                         
            f.write('\n■オーダー一覧' )
            summary = self.order_list().groupby('code')
            for code, group in summary:
                name = master.loc[code]['商品名']
                price = master.loc[code]['価格']
                f.write('\n{}({:,}円): {:,}個'.format(name, price, group.sum()['qty']))
            
            #お預かり金額を書き出し
            
            f.write('\n■お預かり金額:{:,}円'.format(money))

            #お釣りを書き出し
            f.write('\n■お釣り:{:,}円'.format(max(exchange, 0)))
            f.write('\nありがとうございました。')

###メイン処理
def main():
    # マスタ登録
    item_master = []

    #CSVの読み込み、商品コードをインデックスにしてデータフレームに格納
    master = pd.read_csv('master.csv', header = 0)
    master['商品コード'] = master['商品コード'].astype(str).str.zfill(3)
    master = master.set_index('商品コード')

    #データフレームを商品マスターに書き込み
    for i in range(len(master)):
        code = master.index[i]
        item_master.append(Item(code, master.loc[code][0], master.loc[code][1]))

    #オーダー登録
    order = Order(item_master)
    order_end = "No"

    while order_end == "No":
        print('オーダーを(商品コード 個数)の順で入力してください。入力が終われば「yes」を入力してください')
        add_item = input()
        
        if add_item != "yes":
            print('オーダーの個数を入力してください。')
            add_qty = input()
            order.add_item_order('{} {}'.format(add_item, add_qty))
        else:
            order_end = "yes"

    #オーダー表示
    print("■オーダー一覧")
    order.view_item_list(master)

    #オーダーサマリー
    print("■オーダーサマリー")
    order_summary = order.view_order_summary(master)

    #合計金額を表示
    ttl = order.calc_order_ttl(master, order_summary)

    #代金の授受、お釣りを伝える
    money, exchange = order.calc_payment(ttl)

    #レシートを出力
    order.receipt(master, money, exchange)

if __name__ == "__main__":
    main()