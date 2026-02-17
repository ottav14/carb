<script>
	import { onMount } from 'svelte';
	import Dropdown from './Dropdown.svelte';
	import Searchbox from './Searchbox.svelte';

	const dropdownItems = [ 'a', 'b', 'c' ];

	let suggestions = [];
	let tickers;
	let tickerInput;
	let canvas;
	let autocomplete = false;
	let volume;
	let marketCap;

	const handleInput = (e) => {
		const query = e.detail.target.value.toUpperCase();
		if(tickers && query.length)
			suggestions = tickers.filter(ticker => ticker.startsWith(query)).slice(0, 5);
	}

	const line = (x1, y1, x2, y2, ctx) => {
		ctx.beginPath();
		ctx.moveTo(x1, y1);
		ctx.lineTo(x2, y2);
		ctx.stroke();
	}

	const getLow = (prices) => {
		let low = 1000000;
		for(const price of prices) low = price < low ? price : low;
		return low;
	}

	const getHigh = (prices) => {
		let high = 0;
		for(const price of prices) high = price > high ? price : high;
		return high;
	}

	const drawGraph = (prices, canvas) => {
		const ctx = canvas.getContext('2d');
		const n = prices.length-1;
		const low = getLow(prices);
		const high = getHigh(prices);
		ctx.strokeStyle = '#ededed';
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		for(let i=0; i<n; i++) {
			const x1 = i * canvas.width / n;
			const x2 = (i+1) * canvas.width / n;
			const y1 = canvas.height * (prices[i] - low) / (high - low);
			const y2 = canvas.height * (prices[i+1] - low) / (high - low);
			line(x1, y1, x2, y2, ctx);
		}
	}

	const getPrices = (data) => {
		const prices = [];
		for(const point of data)
			prices.push(point.price);
		return prices;
	}

	const apiCall = async (url) => {
		const res = await fetch(url);
		return res.json();
	}

	const setTicker = async (ticker) => {
		autocomplete = false;

		const data = await apiCall(`/api/data/ticker/${ticker}/coinbase`);
		const prices = getPrices(data);
		volume = data.slice(-1)[0].volume.toFixed(2);
		drawGraph(prices, canvas);
	}

	const getTickers = (data) => {
		const tickers = [];
		for(const point of data)
			tickers.push(point.ticker);
		return tickers;
	}

	onMount(async () => {
		const tickerData = await apiCall('/api/tickers/coinbase');
		tickers = getTickers(tickerData);
		setTicker(tickers[0]);
	});

</script>

<main>
	<div id="leftContainer">
		<div class="controls">
			<Dropdown value="test" items={dropdownItems} />
			<Searchbox 
				placeholder="Enter a ticker..." 
				suggestions={suggestions} 
				on:input={(e) => handleInput(e)}
				on:mousedown={(e) => setTicker(e.detail.target.innerText)}
			/>
		</div>
		<canvas bind:this={canvas} />
	</div>
	<div id="stats">
		<p>Volume: {volume}</p>
	</div>
</main>

<style>
	main {
		display: flex;
		border: 1px solid #1f1f1f;		
		margin-right: 2rem;
		font-size: 24pt;
	}

	canvas {
		width: 50rem;
		padding: 2rem;
	}

	.controls {
		display: flex;
		width: max-content;
		position: relative;
		padding: 1rem;
		padding-bottom: 0;
	}


	#ticker {
		padding: 1rem;
	}

	#stats {
		display: flex;
		justify-content: center;
		width: 15rem;
		border-left: 1px solid #1f1f1f;
		font-size: 20pt;
		padding: 1rem;
	}

	#leftContainer {
		flex-grow: 1;
	}
</style>
