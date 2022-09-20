Element.prototype.remove = function () {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function () {
    for (var i = this.length - 1; i >= 0; i--) {
        if (this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

var account = null


document.addEventListener('DOMContentLoaded', (event) => {

    var use_token_field = document.getElementsByName("use_token");
    var selected = document.getElementById('item_selection');
    var amount = document.getElementById('amount');
    var btnBuyConfirm = document.getElementById('btn-buy-confirm');
    var btnBuy = document.getElementById('btn-buy');
    var btnCoinInfo = document.getElementById('btn-coin-info');
    var btnBlockInfo = document.getElementById('btn-block-info');
    var coin_info_field = document.getElementById('coin-info');
    var block_info_field = document.getElementById('block-info');
    var wallet_field = document.getElementById('wallet-info');
    var cart = document.getElementById('cart-info');
    var add_item = document.getElementById('btn-add');
    var btnBindWallet = document.getElementById('btn-bind-wallet');
    var UnbindWalletArea = document.getElementById('btn-disconnect-field');
    var btnCheckAccountBinding = document.getElementById('btn-account-binding-info');


    available_items = [];
    item_dict = {};


    items_in_cart = [];


    cart_item_counter = 0;




    $.ajax({
        type: "GET",
        url: "/get_all_products",
        contentType: "application/json",
        dataType: 'json',
        success: (result) => {
            available_items = result.items;

            var htmlStr = '';
            result.items.forEach(item => {
                htmlStr += '<option value="' + item[0] + '">' + item[item.length - 1] + '</option>';
                item_dict[item[0]] = {
                    "name": item[0],
                    "price": item[2],
                    "reward": item[3],
                }
            });

            if (selected) {
                selected.insertAdjacentHTML("afterbegin", htmlStr);
            } else {
                console.log('item list is null');
            }





        }
    });


    btnBindWallet.addEventListener('click', async () => {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        account = accounts[0];
        console.log(account)

        wallet_field.insertAdjacentHTML("afterbegin", '<p id="wallet_display"> Your Connected Wallet: ' + account + '<p/>');

        UnbindWalletArea.insertAdjacentHTML("afterbegin", '<button id="btn-unbind-wallet">Disconnect Your Wallet</button>');
        document.getElementById('btn-unbind-wallet').addEventListener('click', () => {
            //remove wallet and buttom, use child element of the DOM div

            wallet_field.childNodes.remove();
            UnbindWalletArea.childNodes.remove();
            account = null;
        })

    });


    btnBuy.addEventListener('click', () => {

        var use_token = use_token_field[0].checked ? true : false;
        var server_data = {
            "items_chosen": items_in_cart,
            "use_token": use_token,
            "uname": client_name,
            // "selected_item": selected_item,
            "wallet": account,
            // "amount": amount_to_buy
        };

        console.log('btn-buy clicked');

        $.ajax({
            type: "POST",
            url: "/order_directly",
            data: JSON.stringify(server_data),
            contentType: "application/json",
            dataType: 'json',
            success: (result) => {
                alert(result.message);

            }
        });
    });



    //this entire function need to be modified
    btnBuyConfirm.addEventListener('click', () => {
        var use_token = use_token_field[0].checked ? true : false;
        // var selected_item = selected.value;
        // var amount_to_buy = amount.value;
        // console.log(use_token);
        // console.log(selected_item);
        // console.log(amount_to_buy);
        // console.log(client_name);
        // console.log(client_wallet);

        console.log('btn-buy-confirm clicked');


        var server_data = {
            "items_chosen": items_in_cart,
            "use_token": use_token,
            "uname": client_name,
            // "selected_item": selected_item,
            "wallet": account,
            // "amount": amount_to_buy
        };

        $.ajax({
            type: "POST",
            url: "/order",
            data: JSON.stringify(server_data),
            contentType: "application/json",
            dataType: 'json',
            success: (result) => {
                alert(result.message);
                switch (result.status) {
                    case 0:
                        break;
                    case 1:
                        ethereum
                            .request({
                                method: 'eth_sendTransaction',
                                params: [
                                    {
                                        from: account,
                                        data: result.functionData,
                                        gasPrice: '0x09184e72a000',
                                        gas: '0x5208',
                                        gasLimit: '0x71d75ab9b920500000'


                                    },
                                ],
                            })
                            .then((txHash) => console.log(txHash))
                            .catch((error) => console.error);
                        break;
                }


            }
        });
    });



    function construct_cart_item_html(each_item) {
        cart_item_counter++;

        return '<div class="row"><div class="col-4"><p>' + each_item.item + '.   Amount: ' + each_item.amount + '.   Total Price: ' + each_item.price + '</p></div>'
            + "<div class='col-2'><button  id = 'cart_item_" + (cart_item_counter) + "'>Delete</button></div>"
            + '<hr></div>';
    }



    add_item.addEventListener('click', () => {
        var selected_item = selected.value;
        var amount_to_buy = amount.value;
        var selected_item_info = item_dict[selected_item];
        var new_item = { "item": selected_item_info.name, "price": selected_item_info.price * amount_to_buy, "amount": amount_to_buy };
        items_in_cart.push(new_item);
        // alert(selected_item_info.name);
        var temp = construct_cart_item_html(new_item);
        // console.log(temp);
        // console.log(items_in_cart);
        cart.insertAdjacentHTML('afterbegin', temp);
        if (!cart) { console.log("cart is deleted") };

        var deletebtn = document.getElementById('cart_item_' + (cart_item_counter));
        if (!deletebtn) { console.log("cant get it") };
        deletebtn.myParam = deletebtn.parentElement.parentElement;
        deletebtn.addEventListener('click', (elem) => {
            // console.log(elem);
            cart.removeChild(elem.currentTarget.myParam);
            var temp = items_in_cart.indexOf(new_item);
            // console.log(temp);
            var removed_item = items_in_cart.splice(temp, 1);
            console.log(removed_item);
            console.log(cart_item_counter);
            console.log(items_in_cart);
            // console.log(items_in_cart);
            // console.log(item_dict);
        })

    });

    btnCoinInfo.addEventListener('click', () => {



        $.ajax({
            type: "GET",
            url: "/user_coin_info/" + client_name + "/" + client_wallet,
            // data: JSON.stringify(server_data),
            contentType: "application/json",
            dataType: 'json',
            success: (result) => {
                var coinInfo = '<p> balance of ' + result.name + ' is : ' + result.balance + ' . Balance checked at: ' + new Date() + '</p><hr>';
                coin_info_field.insertAdjacentHTML('afterbegin', coinInfo);

            }
        });
    });

    btnCheckAccountBinding.addEventListener('click', () => {
        if (account) {
            alert("current account : " + account);
        } else {
            alert("account not detected");
        }
    });


    btnBlockInfo.addEventListener('click', () => {



        $.ajax({
            type: "GET",
            url: "/latest_block",
            // data: JSON.stringify(server_data),
            contentType: "application/json",
            dataType: 'json',
            success: (result) => {
                block_info_field.innerHTML = '';
                for (const key in result) {
                    if (Object.hasOwnProperty.call(result, key)) {
                        const element = result[key];
                        console.log(key);
                        console.log(element);

                        block_info_field.insertAdjacentHTML('beforeend', '<p>' + key + ' : ' + element + '</p><hr>');
                    }
                }

                block_info_field.insertAdjacentHTML('beforeend', "<br><br>");



            }
        });
    });
});


