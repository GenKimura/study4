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
    
    def add_item_order(self, item_code):
        self.item_order_list.append(item_code)
    
    def view_item_list(self):
        for item in self.item_order_list:
            name = self.item_master[int(item)-1].get_name()
            price = self.item_master[int(item)-1].get_price()
            
            print("商品コード：{} 商品名：{} 価格：{}".format(item, name, price))

###メイン処理
def main():
    # マスタ登録
    item_master = []
    item_master.append(Item("001", "りんご", 1000))
    item_master.append(Item("002", "なし", 120))
    item_master.append(Item("003", "みかん", 150))

    #オーダー登録
    order = Order(item_master)
    order_end = "No"

    while order_end == "No":
        print('オーダーを商品コードで入力してください。入力が終われば「yes」を入力してください')
        add_item = input()
        
        if add_item != "yes":
            order.add_item_order(add_item)
        else:
            order_end = "yes"

    #オーダー表示
    order.view_item_list()

if __name__ == "__main__":
    main()