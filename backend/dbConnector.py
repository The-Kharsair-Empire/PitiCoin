from logging import fatal
import mysql.connector
import mysql.connector.errorcode as errorcode

# mysql -u root -p 99999999


class DBWrapper:
    def __init__(
        self,
        username="kharsair",
        host_addr="localhost",
        psw="MySQL_10061",
        db_name="demo",
        **kwargs,
    ) -> None:
        self.db = mysql.connector.connect(
            user=username,
            password=psw,
            host=host_addr,
            database=db_name,
        )
        self.cursor = self.db.cursor()

    def insert_entry(self, table_name, **kwargs):
        keys = []
        values = []
        for i in kwargs:
            keys.append(i)
            values.append(kwargs[i])

        keys = ",".join(keys)
        values = tuple(values)
        # place_holder = ",".join(["%s" for _ in range(len(values))])
        values = ','.join(
            list(map(lambda x: str(x) if (not isinstance(x, str) or x.endswith('()')) else "'"+x+"'", values))
            )
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({values});"
        print(query, " -> being executed")
        
        try:
            self.cursor.execute(query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def delete_entry(self, table_name, conditions):
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        try:
            self.cursor.execute(query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def clear_table(self, table_name):
        query = f"""
                TRUNCATE {table_name};
                DELETE FROM {table_name};
            """
        try:
            self.cursor.execute(query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def run_query(self, query):
        try:
            print(query)
            self.cursor.execute(query)
            entries = self.cursor.fetchall()
            return entries
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    # user by the server to fetch items, users and display for user to choose
    def get_table(self, table_name, condition=None, select_filter=None):
        query = f"SELECT {select_filter if select_filter else '*'} FROM {table_name}{' ' + condition + ';' if condition else ';'}"
        try:
            print(query)
            self.cursor.execute(query)
            entries = self.cursor.fetchall()
            # for i in self.cursor:
            #     entries.append(i)
            return entries
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def get_user(self, username, key_index=None):
        query = f"SELECT * FROM Customer WHERE name = '{username}'"
        try:
            print(query)
            self.cursor.execute(query)
            user = self.cursor.fetchone()
            if key_index is not None:
                return user[key_index]
            return user
            # for i in self.cursor:
            #     return i  # username is unique entry
            # return None
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def get_item(self, item_name):
        query = f"SELECT * FROM Item WHERE name = '{item_name}'"
        try:
            print(query)
            self.cursor.execute(query)
            item = self.cursor.fetchone()
            return item
            # for i in self.cursor:
            #     return i  # username is unique entry
            # return None
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def get_specific_value(self, table, name, *columns):

        col = ",".join(columns)

        query = f"SELECT ({col}) FROM {table} WHERE name = '{name}'"
        try:
            print(query)
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("syntax error!")
            else:
                print("Error: {}".format(err))

    def commit(self):
        try:
            self.db.commit()
        except Exception as e:
            print(e)


if __name__ == "__main__":

    db = DBWrapper()
    # db.clear_table("Contract")
    db.insert_entry("Contract", token_symbol='JDC', value_to_ether = 0.47,
                    contract_addr='0x3c6b18C7E55C2e819B1e04ad8caB7406Ae79b027',
                    contract_network='http://192.168.0.2:8545',
                    fullname='joidea coin',
                    contract_abi_path='/home/kharsair/Documents/blockchain/token/build/contracts/JoideaCoin.json')

    db.insert_entry("Contract", token_symbol='KSC', value_to_ether = 1.15,
                    contract_addr='0xdD17970F9a24f737611ed6F01aF6C07B7E82A563',
                    contract_network='http://192.168.0.2:8545',
                    fullname='kharsair coin',
                    contract_abi_path='/home/kharsair/Documents/blockchain/token/build/contracts/KharsairCoin.json')
    # db.commit()

    # print(db.get_table("Item"))

  

    db.insert_entry(
        "Item", name="SmallItem", price_ether=100, reward_ether=10,
        description="Small item, 100 ether get 10 ether worth of reward in jdc"
    )
    db.insert_entry(
        "Item", name="LargeItem", price_ether=200, reward_ether=20,
        description="Large item, 200 ether get 20 ether worth of reward in jdc"
    )
    db.insert_entry(
        "Item", name="ExtraLargeIten", price_ether=400, reward_ether=40,
        description="Extra large item, 400 ether get 40 ether worth of reward in jdc"
    )

    db.commit()

    # db.clear_table("Item")


# CREATE TABLE Item (name VARCHAR(50) UNIQUE, ID int PRIMARY KEY AUTO_INCREMENT, price_ether int UNSIGNED, reward_ether int UNSIGNED, description VARCHAR(250));
# CREATE TABLE Customer (name VARCHAR(50) UNIQUE, ID int PRIMARY KEY AUTO_INCREMENT, password VARCHAR(64), wallet VARCHAR(42));
# CREATE TABLE CustomerOrder (ID int PRIMARY KEY AUTO_INCREMENT, date_time DATETIME, Orderred_by int, status VARCHAR(50), FOREIGN KEY (Orderred_by) REFERENCES Customer (ID));
# CREATE TABLE Contract (token_symbol VARCHAR(10) PRIMARY KEY , value_to_ether decimal(20, 10), contract_addr VARCHAR(42), contract_network VARCHAR(100), fullname VARCHAR(50), contract_abi_path VARCHAR(200));
# CREATE TABLE Transaction (ID int PRIMARY KEY AUTO_INCREMENT, Order_ID int, FOREIGN KEY (Order_ID) REFERENCES CustomerOrder (ID), date_time datetime, Purchase_with VARCHAR(10) , FOREIGN KEY (Purchase_with) REFERENCES Contract (token_symbol), value int);
# CREATE TABLE OrderLineItem (ID int PRIMARY KEY AUTO_INCREMENT, Order_ID int, FOREIGN KEY (Order_ID) REFERENCES CustomerOrder (ID), Item_ID int, FOREIGN KEY (Item_ID) REFERENCES Item (ID));
# CREATE TABLE ExchangeRate (token0 VARCHAR(10), token1 VARCHAR(10), rate decimal(20, 10), pair VARCHAR(20) PRIMARY KEY, FOREIGN KEY (token0) REFERENCES Contract (token_symbol), FOREIGN KEY (token1) REFERENCES Contract (token_symbol));
# CREATE TABLE Transaction (ID int PRIMARY KEY AUTO_INCREMENT, Order_ID int, FOREIGN KEY (Order_ID) REFERENCES CustomerOrder (ID), date_time datetime, Purchase_with ENUM('AUD', 'JDC'), value int);
