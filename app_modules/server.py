from re import U
from unittest.mock import call
from flask import json, url_for
from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from markupsafe import escape
import web3
from coin import Coin
from dbConnector import DBWrapper

print("take 1")  # test
db = DBWrapper()


def get_price_in_aud(price_in_ether: int) -> int:
    return price_in_ether


def initialize_coin():

    coins = {}
    f = open("serverConfigs.json")
    configs = json.load(f)
    f.close()

    contract_name = configs["contract_name"]
    contract_addr = configs["contract_addr"]
    server_addr = configs["ethereum_network_addr"]
    abi_path = configs["abi_path"]

    for i, name in enumerate(contract_name):
        coins[name] = Coin(
            contract_addr[i],
            abi_path[i],
            name,
            server_addr[i]
        )

    return coins


coins = initialize_coin()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    return render_template("index.html")


@app.route("/get_all_products", methods=["GET"])
def get_all_products():
    items = db.get_table("Item")

    for each in items:
        print(each)

    return jsonify({"items": items})


@app.route("/order", methods=["POST"])
def order():
    print("order")

    # print()

    data = request.get_json()
    purchased_items = data['items_chosen']
    uname = data['uname']
    use_token = data['use_token']
    client_wallet_address = data['wallet']
    print(client_wallet_address)

    uid = db.get_user(uname, 1)

    db.insert_entry('CustomerOrder', date_time="NOW()",
                    Orderred_by=uid, status='ordered')
    db.commit()
    last_id = db.run_query('SELECT LAST_INSERT_ID();')[
        0][0]  # last inserted "order" id

    total_price = 0
    total_reward = 0
    for e in purchased_items:
        item = e['item']
        price = e['price']
        amount = int(e['amount'])
        db_item_record = db.get_item(item)
        item_id = db_item_record[1]
        reward = int(db_item_record[3])
        if price != db_item_record[2]:
            print("price mismatched")
            print(price)
            print(db_item_record[2])

        for i in range(amount):
            db.insert_entry('OrderLineItem', Order_ID=int(
                last_id), Item_ID=int(item_id))

            total_reward += reward
        total_price += price

    db.commit()
    total_price_aud = get_price_in_aud(total_price)

    client_wallet_address = coins["JDC"].w3.toChecksumAddress(
        client_wallet_address)

    if use_token:
        # coins["JDC"].sendTokenToClient(client_wallet_address, total_reward)
        call_data = coins["JDC"].getTrasactionData(
            'sendTokenFromClient', coins["JDC"].w3.toWei(total_price, "ether"))
        print("call data", end=' : ')
        print(call_data)
        return jsonify({"status": 1, "message": "invoke metamask transaction", "functionData": call_data})
    else:
        coins["JDC"].sendTokenToClient(client_wallet_address, total_reward)
        db.insert_entry("Transaction", Order_ID=int(
            last_id), date_time="NOW()", Purchase_with='AUD', value=int(total_price_aud))
        return jsonify({"status": 0, "message": f"success, you just spent {total_price_aud} AUD, and get {total_reward} ether worth of JDC in reward"})


@app.route("/order_directly", methods=["POST"])
def order_directly():
    print("order directly")

    # print()

    data = request.get_json()
    purchased_items = data['items_chosen']
    uname = data['uname']
    use_token = data['use_token']
    client_wallet_address = data['wallet']
    print(client_wallet_address)

    uid = db.get_user(uname, 1)

    db.insert_entry('CustomerOrder', date_time="NOW()",
                    Orderred_by=uid, status='ordered')
    db.commit()
    last_id = db.run_query('SELECT LAST_INSERT_ID();')[
        0][0]  # last inserted "order" id

    total_price = 0
    total_reward = 0
    for e in purchased_items:
        item = e['item']
        price = e['price']
        amount = int(e['amount'])
        db_item_record = db.get_item(item)
        item_id = db_item_record[1]
        reward = int(db_item_record[3])
        if price != db_item_record[2]:
            print("price mismatched")
            print(price)
            print(db_item_record[2])

        for i in range(amount):
            db.insert_entry('OrderLineItem', Order_ID=int(
                last_id), Item_ID=int(item_id))

            total_reward += reward
        total_price += price

    db.commit()
    total_price_aud = get_price_in_aud(total_price)

    client_wallet_address = coins["JDC"].w3.toChecksumAddress(
        client_wallet_address)

    if use_token:
        coins["JDC"].sendTokenFromClient(client_wallet_address, total_price)
        db.insert_entry("Transaction", Order_ID=int(
            last_id), date_time="NOW()", Purchase_with='JDC', value=int(total_price))
        return jsonify({"status": 0, "message": f"success, you just spent {total_price} JDC"})

    else:
        coins["JDC"].sendTokenToClient(client_wallet_address, total_reward)

        db.insert_entry("Transaction", Order_ID=int(
            last_id), date_time="NOW()", Purchase_with='AUD', value=int(total_price_aud))
        return jsonify({"status": 0, "message": f"success, you just spent {total_price_aud} AUD, and get {total_reward} ether worth of JDC in reward"})


@app.route("/user_coin_info/<username>/<wallet>", methods=["GET"])
def user_coin_info(username, wallet):
    print(username, wallet)
    coin_name = "JDC"
    balance = coins[coin_name].getBalance(wallet)
    return jsonify({"name": coins[coin_name].name, "balance": balance}), 200


@app.route("/verify_user", methods=["POST"])
def verify_user():
    data = request.get_json()
    uname = data["username"]
    upsw_hash = data["password"]
    # wallet = data["address"]
    user_info = db.get_user(uname)
    if user_info:
        # print(user_info[3])
        # print(wallet)

        # if user_info[3].lower() != wallet.lower():
        #     return jsonify({
        #     "status": 1,
        #     "message": "connected wallet differ from the registered one, make sure to connect to the right one, retry",
        #     "username": user_info[0],
        #     "password": user_info[2],
        #     "wallet": user_info[3]
        # })

        return jsonify({
            "status": 0,
            "message": "user found!",
            "username": user_info[0],
            "password": user_info[2],
            # "wallet": user_info[3]
        })
    else:
        return jsonify({
            "status": -1,
            "message": "user not found! go and register",
            "username": None,
            "password": None,
            # "wallet": None
        })


@app.route("/to_shopping/<uname>", methods=["GET"])
def to_shopping(uname):

    # uname = request.args.get('uname')
    # wallet = request.args.get('wallet')
    return render_template(
        "shopping.html",
        # addr=wallet,
        name=uname,

    )


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    uname = data["username"]
    upsw_hash = data["password"]
    # addr = data["address"]
    print("register")
    if len(uname) == 0:
        return jsonify({"status": -1, "message": "blank user name!"})

    # if addr and len(addr) == 42:
    db.insert_entry("Customer", name=uname,
                    password=upsw_hash)  # , wallet=addr)
    db.commit()
    print("user added")
    return jsonify({"status": 0, "message": "successfully registered, now go to login"})
    # else:
    #     return jsonify({"status": -1, "message": "is this a wallet address?, retry"})


@app.route("/switch_to_login", methods=["GET"])
def goto_login():
    print("to login")
    return render_template("index.html")


@app.route("/switch_to_register", methods=["GET"])
def goto_register():
    print("to register")
    return render_template("register.html")


# test section

@app.route("/latest_block", methods=["GET"])
def latest_block():
    retVal = {}
    latest_block = coins["JDC"].getLatestBlock()
    for i in latest_block:
        if isinstance(latest_block[i], bytes):
            retVal[i] = latest_block[i].hex()

        elif i == 'transactions':
            trans = []
            for each in latest_block[i]:
                trans.append(each.hex())
            retVal[i] = trans
        else:
            retVal[i] = latest_block[i]
    print(retVal)

    return jsonify(retVal)


if __name__ == "__main__":
    app.run(debug=True)
