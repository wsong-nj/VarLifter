// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvestmentFund {
    mapping(address => uint256) public shares;
    mapping(address => uint256) public balanceOf;
    uint256 public totalShares;
    uint256 public totalBalance;

    function buyShares(uint256 _amount) public payable {
        shares[msg.sender] += _amount;
        balanceOf[msg.sender] += msg.value;
        totalShares += _amount;
        totalBalance += msg.value;
    }

    function sellShares(uint256 _amount) public {
        require(shares[msg.sender] >= _amount, "Insufficient shares");

        uint256 sharePrice = totalBalance / totalShares;
        uint256 saleValue = sharePrice * _amount;
        shares[msg.sender] -= _amount;
        balanceOf[msg.sender] -= saleValue;
        totalShares -= _amount;
        totalBalance -= saleValue;

        payable(msg.sender).transfer(saleValue);
    }
}
