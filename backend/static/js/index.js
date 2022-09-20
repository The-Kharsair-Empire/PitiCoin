var loginBtn = document.getElementById('btn-login');
var gotoBtn = document.getElementById('btn-goto-register');
loginBtn.addEventListener('click', async () => {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var msg_area = document.getElementById('feedback-msg');

    

    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
    const account = accounts[0];

    var server_data = {
        "username": username,
        "password": password,
        "address" : account
    }

    $.ajax({
        type: "POST",
        url: "/verify_user",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: (result) => {
            if (result.status >= 0) {
                console.log(password);
                console.log(result.password);
                console.log(password == result.password);
                if (username == result.username && password == result.password) {
                    if (result.status == 1)
                    {
                        alert(`warning: ${result.message}`);
                    } else
                    {
                        $(location).attr('href', '/to_shopping/' + username + '/' + result.wallet);
                    }
                    
                } else {
                    alert("incorrect password, retry");
                }
            } else {
                alert(result.message);
                $(location).attr('href', '/switch_to_register');
            }

        }
    });


});

gotoBtn.addEventListener('click', () => {
    $(location).attr('href', '/switch_to_register');

})