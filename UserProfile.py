import pickle


class User:
    def __init__(self, data):
        self.info = data  #object is not subscriptable
        self.changes = False

    def addToFav(self, stock_name):
        self.info["Favorites"].append(stock_name)
        self.changes = True
        return True

    def purchaseStock(self, stock_name, stock_price, quantity):
        ############
        # 1. Check if user has sufficient money if he has than add to his stock list and subtract from his wallet
        # 2. It return true if everything went good(purchase happend successfully) else returns False
        #######
        if (self.isSufficient(stock_price)):
            data = self.info["MyStock"].setdefault(stock_name,
                                                   [stock_price, quantity])
            if (len(data) > 0):
                data[0] += stock_price
                data[1] += quantity
            # self.info["Wallet"] -= stock_price
            self.changes = True
            return True
        return False

    def currentCash(self):
        # Return amount of money user have
        return self.info["Wallet"]

    def isSufficient(self, stock_price):
        # Returns if user has sufficient amount of money to purchase stock
        return False if (self.currentCash() < stock_price) else True

    def logout(self):
        # This is delete the user data locally
        with open(
                "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/user.txt",
                'wb') as f:
            f.close()

    def __del__(self):
        ###############
        # If any changes store locally as well as in database
        # user del object_name to call destructor or it'll happen automatically
        # ########
        # print("I'm getting destoryed.")
        if (self.changes):
            with open(
                    "C:/Users/shyam/Documents/aditya/Project/Programs/NoobStock/user.txt",
                    'wb') as f:
                f.write(pickle.dumps(self.info))
                print("Im done writing")
                f.close()


# a = User({
#     "Name": "",
#     "NickName": "",
#     "Wallet": 10000,
#     "Favorites": [],
#     "MyStocks": [],
#     "UserID": 0,
#     "SessionValid": True
# })
# a.info["Favorites"].append("It's me")
# print(a.info["Favorites"])