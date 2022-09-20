var regiBtn = document.getElementById('btn-register');
var gotoBtn = document.getElementById('btn-goto-login');
regiBtn.addEventListener('click', async () => {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var msg_area = document.getElementById('feedback-msg');

    if (typeof window.ethereum !== 'undefined') {
        console.log('MetaMask is installed!');
    }



    

    // const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
    // const account = accounts[0];
    // console.log(account)

    var server_data = {
        "username": username,
        "password": password,
        // "address": account
    }

    $.ajax({
        type: "POST",
        url: "/register",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            switch (result.status) {
                case -1:
                    alert(result.message)
                    break;
                case 0: {
                    
                    alert(result.message)
                    $(location).attr('href', '/switch_to_login');
                }
                    break;
                default:
                    alert("must be server code logic error huh..");
            }


        }
    });


});

gotoBtn.addEventListener('click', () => {
    $(location).attr('href', '/switch_to_login');
})