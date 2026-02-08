<script>
	import { onMount } from 'svelte';
	import Dropdown from './components/Dropdown.svelte';

	let suggestions = [];
	let query = '';
	let ticker;
	let tickers;

	$: if(query) {
		query = query.toUpperCase();
		if(query.length)
			suggestions = tickers.filter(ticker => ticker.startsWith(query)).slice(0, 5);
		else
			suggestions = [];
	}

	const apiCall = async (url) => {
		const res = await fetch(url);
		return res.json();
	}

	const getTickerID = async (ticker) => {
		const data = await apiCall(`/api/id/${ticker}`);
		return data[0].id;
	}

	const getPrices = (data) => {
		const prices = [];
		for(const point of data)
			prices.push(point.price);
		return prices;
	}

	const getTickers = (data) => {
		const tickers = [];
		for(const point of data)
			tickers.push(point.ticker);
		return tickers;
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

	const setTicker = async (t) => {
		ticker = t;
		suggestions = [];
		query = '';

		const id = await getTickerID(ticker);
		const data = await apiCall(`/api/data/${id}`);
		const prices = getPrices(data);
		const canvas = document.querySelector('canvas');
		drawGraph(prices, canvas);
	}

	onMount(async () => {


		const tickerData = await apiCall('/api/tickers');
		tickers = getTickers(tickerData);
		ticker = tickers[0];
		const id = tickerData[0].id;

		const data = await apiCall(`/api/data/${id}`);
		const prices = getPrices(data);

		const canvas = document.querySelector('canvas');
		const ctx = canvas.getContext('2d');

		canvas.width = 512;
		canvas.height = 256;

		drawGraph(prices, canvas);
	});
</script>

<main>
	<div id="display">
		<div class="controls">
			{#if ticker}
				<p>{ticker}</p>
			{/if}
			<input type="text" bind:value={query} placeholder="Enter ticker..." />
			{#if suggestions.length}
				<ul class="autocomplete">
					{#each suggestions as s}
						<li on:click={() => setTicker(s)} class="suggestion">{s}</li>
					{/each}
				</ul>
			{/if}
		</div>
		<canvas />
	</div>
</main>

<style>
	main {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		background-color: #000;
		color: #ededed;
		font-family: "sans-serif";
	}

	canvas {
		padding: 2rem;
	}

	.controls {
		display: flex;
		flex-direction: column;
		width: max-content;
		position: relative;
	}

	.autocomplete {
		position: absolute;
		width: 100%;
		padding: 0;
		top: 100%;
		list-style: none;
		background-color: #000;
	}

	.suggestion {
		padding: 0.5rem;
	}

	.suggestion:hover {
		background-color: #1f1f1f;
	}

	#ticker {
		padding: 1rem;
	}

	#display {
		display: flex;
		flex-direction: column;
		border: 1px solid #1f1f1f;		
	}
</style>
