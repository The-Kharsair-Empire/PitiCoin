// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract JoideaCoin is ERC20 {
    address public admin;
    uint256 public cap;

    constructor() ERC20("JoideaCoin", "JDC") {
        admin = msg.sender;
        cap = 20000;
        _mint(msg.sender, 10000 * (10**18));
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == admin, "you are not admin, die!");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == admin, "you are not admin, die!");
        _burn(from, amount);
    }

    event tokenTransferredToClient(address client, uint256 amount);
    event tokenTransferredBackToAdmin(address client, uint256 amount);
   

    function sendTokenToClient(uint256 amount) external {
        require(msg.sender != admin, "admin should not send to yourself");
        require(this.balanceOf(admin) >= amount, "not enough token");
        _transfer(admin, msg.sender, amount);
        emit tokenTransferredToClient(msg.sender, amount);
    }

    function sendTokenFromClient(uint256 amount) external {
        require(msg.sender != admin, "admin should not send to itself");
        require(this.balanceOf(msg.sender) >= amount, "not enough token");
        _transfer(msg.sender, admin, amount);
        emit tokenTransferredBackToAdmin(msg.sender, amount);
    }



    //for testing
    event eventFired(address reader);
    event secondEvent(address caller, address origin);
    event revealBalances(uint256 senderBalance, uint256 recipientBalance);

    function calledByContract() internal {
        emit secondEvent(msg.sender, tx.origin);
    }

    function testEvent() external {
        emit eventFired(msg.sender);
        calledByContract();
    }

    function getAdmin() external view returns (address) {
        return admin;
    }

    function checkBalance(address sender, address recipient)
        external
        returns (uint256, uint256)
    {
        uint256 senderBalance = this.balanceOf(sender);
        uint256 recipientBalance = this.balanceOf(recipient);

        emit revealBalances(senderBalance, recipientBalance);
        return (senderBalance, recipientBalance);
    }
}
