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
    
    def view_item_list(self):
        for item in self.item_order_list:
            item_code = item.split()[0]
            item_qty = item.split()[1]
            name = self.item_master[int(item_code)-1].get_name()
            price = self.item_master[int(item_code)-1].get_price()
            
            print("商品コード：{} 商品名：{} 価格：{}  ×　{}個".format(item_code, name, price, item_qty))

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
            order.add_item_order(add_item)
        else:
            order_end = "yes"

    #オーダー表示
    order.view_item_list()

if __name__ == "__main__":
    main()