const JoideaCoin = artifacts.require("JoideaCoin");
const KharsairCoin = artifacts.require("KharsairCoin");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("JoideaCoin", function (/* accounts */) {
  it("should assert true", async function () {
    await JoideaCoin.deployed();
    return assert.isTrue(true);
  });
});


contract("KharsairCoin", function (/* accounts */) {
  it("should assert true", async function () {
    await KharsairCoin.deployed();
    return assert.isTrue(true);
  });
});
