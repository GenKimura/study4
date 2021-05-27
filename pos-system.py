import datetime
import pandas as pd

###　商品クラス
class Item:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price
    
    def get_name(self):
        return self.item_name
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self, item_master):
        self.item_order_list = []
        self.item_master = item_master
    
    #オーダーの商品コード、数量を追加
    def add_item_order(self, item_ordered):
        self.item_order_list.append(item_ordered)
    
    #商品コードから商品情報が入ったItemインスタンスを取得
    def get_item_info(self, code):
        for i in self.item_master:
            if code == i.item_code:
                return i

    #注文をすべて表示
    def view_item_list(self):
        for o in self.item_order_list:
            info = self.get_item_info(o['code'])
            print('　Code:{}, Name:{:>3}, Price:{:>5,}円, Qty:{:>3,}個'.format(info.item_code, info.item_name, info.price, o['qty']))
    
    #商品ごとの数量合計、小計、オーダーの費用合計を表示
    def order_summary(self):
        ttl = 0
        summary = pd.DataFrame.from_dict(self.item_order_list).groupby('code').sum()
        for i in range(len(summary)):
            info = self.get_item_info(summary.index[i])
            qty = summary.iloc[i]['qty']
            subttl = info.price * qty
            ttl += subttl
            print('　Code:{}, Name:{:>3}, Price:{:>5,}円, Qty:{:>3,}個, Subttl:{:>8,}円'.format(info.item_code, info.item_name, info.price, qty, subttl))
        print('  合計金額:{:>7,}円'.format(ttl))
        return ttl
    
    #代金の授受
    def payment(self, ttl):
        payment_done = False
        
        while payment_done == False:
            money = int(input('受け取った代金を入力して下さい'))
            exchange = money - ttl
            
            if money == ttl:
                print('ありがとうございました。ちょうどお預かりします。')
                payment_done = True
            elif money > ttl:
                print('ありがとうございました。{:,}円のお返しです。'.format(exchange))
                payment_done = True
            else:
                print('お代が足りません。')
        return money, exchange

    def receipt(self, money, exchange):
        with open('receipt.txt', 'w', encoding='UTF-8') as f:
        #日付
            dt_now = datetime.datetime.now()
            f.write(dt_now.strftime('%Y/%m/%d %H:%M:%S'))
        
        #オーダー一覧を書き出し                         
            f.write('\n■オーダー一覧' )
            summary = pd.DataFrame.from_dict(self.item_order_list).groupby('code').sum()
            for i in range(len(summary)):
                info = self.get_item_info(summary.index[i])
                qty = summary.iloc[i]['qty']
                subttl = info.price * qty
                f.write('\n　Code:{}, Name:{:>3}, Price:{:>5,}円, Qty:{:>3,}個, Subttl:{:>8,}円'.format(info.item_code, info.item_name, info.price, qty, subttl))

        #お預かり金額を書き出し
            f.write('\n■お預かり金額:{:>7,}円'.format(money))
        
        #お釣りを書き出し
            f.write('\n■お釣り:{:>7,}円'.format(max(exchange, 0)))
            f.write('\nありがとうございました。')


###メイン処理
def main():
     #商品マスターCSVを読み込み、OrderクラスのItem_masterに登録
    item_master = []
    
    master = pd.read_csv('master.csv', header = 0)
    master['商品コード'] = master['商品コード'].astype(str).str.zfill(3)
    master = master.set_index('商品コード')
    
    for i in range(len(master)):
        code = master.index[i]
        item_master.append(Item(code, master.loc[code][0], master.loc[code][1]))
    
    #オーダー登録
    order = Order(item_master)
    order_done = 'n'
    
    while order_done != 'y':
        add_code = input('オーダーの商品コードを入力してください')
        add_qty = int(input('個数を入力してください'))
        order.add_item_order({'code': add_code, 'qty': add_qty})
        order_done = input('オーダーは完了ですか？ (Yes: y, No: n)')
    
    print('■オーダー一覧')
    order.view_item_list()

    print('■オーダー合計')
    ttl = order.order_summary()
    
    #代金授受
    money, exchange = order.payment(ttl)
    
    #レシートを出力
    order.receipt(money, exchange)

if __name__ == "__main__":
    main()