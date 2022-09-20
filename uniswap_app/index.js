const {ChainId, Fetcher, WETH, Route} = require('@uniswap/sdk');


const chainId = ChainId.ROPSTEN;

// const tokenAddr = '0x4C3a9E840f801c96A5a2dE5c5aC8ad3B8Fa8D22C';
const tokenAddr = '0xad6d458402f60fd3bd25163575031acdce07538d';
// const tokenAddr = '0x6B175474E89094C44Da98b954EedeAC495271d0F';

const init = async () => {
    const jdc = await Fetcher.fetchTokenData(chainId, tokenAddr);
    console.log(jdc.address);
    console.log(jdc.chainId);
    console.log(jdc.name);

    const weth = WETH[chainId];
    const pair = await Fetcher.fetchPairData(jdc, weth);

    const route = new Route([pair], weth);

    console.log(route.midPrice.toSignificant(6));
    console.log(route.midPrice.invert().toSignificant(6));
}

init();



document.getElementById('get-pair').addEventListener('click', () => {
    document.getElementById("pair").insertAdjacentHTML('afterbegin', "<p>" + route.midPrice.toSignificant(6) + ":" + route.midPrice.invert().toSignificant(6) +"</p>")
});
