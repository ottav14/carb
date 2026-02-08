<script>
	import { onMount } from 'svelte';

	let suggestions = [];
	let query = '';
	let ticker;
	let tickers;
	let canvas;

	$: if(query) {
		query = query.toUpperCase();
		if(query.length)
			suggestions = tickers.filter(ticker => ticker.startsWith(query)).slice(0, 5);
		else
			suggestions = [];
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

	const getTickerID = async (ticker) => {
		const data = await apiCall(`/api/id/${ticker}`);
		return data[0].id;
	}

	const setTicker = async (t) => {
		ticker = t;
		suggestions = [];
		query = '';

		const id = await getTickerID(ticker);
		const data = await apiCall(`/api/data/${id}`);
		const prices = getPrices(data);
		drawGraph(prices, canvas);
	}

	const getTickers = (data) => {
		const tickers = [];
		for(const point of data)
			tickers.push(point.ticker);
		return tickers;
	}

	onMount(async () => {
		const tickerData = await apiCall('/api/tickers');
		tickers = getTickers(tickerData);
		ticker = tickers[0];
		const id = tickerData[0].id;

		const data = await apiCall(`/api/data/${id}`);
		const prices = getPrices(data);

		const ctx = canvas.getContext('2d');

		drawGraph(prices, canvas);
	});

</script>

<main>
	<div class="controls">
		{#if ticker}
			<p id="ticker">{ticker}</p>
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
	<canvas bind:this={canvas} />
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		border: 1px solid #1f1f1f;		
		width: 50rem;
		margin-right: 2rem;
		font-size: 24pt;
	}

	input {
		height: 2rem;
		font-size: 24pt;
	}

	canvas {
		padding: 2rem;
	}

	.controls {
		display: flex;
		flex-direction: column;
		width: max-content;
		position: relative;
		padding: 1rem;
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
</style>
