// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Donation {
    address public owner;
    mapping(address => uint256) public donations;

    event DonationReceived(address donor, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    function donate() public payable {
        require(msg.value > 0, "Donation must be greater than 0");

        donations[msg.sender] += msg.value;
        emit DonationReceived(msg.sender, msg.value);
    }

    function withdraw() public {
        require(msg.sender == owner, "You are not the owner");
        payable(owner).transfer(address(this).balance);
    }

    function checkDonation(address donor) public view returns (uint256) {
        return donations[donor];
    }
}
