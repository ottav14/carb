<script>
	import { onMount } from 'svelte';

	let ticker;

	const apiCall = async (url) => {
		const res = await fetch(url);
		return res.json();
	}

	const getPrices = (data) => {
		const prices = [];
		for(const point of data)
			prices.push(point.price);
		return prices;
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
		for(let i=0; i<n; i++) {
			const x1 = i * canvas.width / n;
			const x2 = (i+1) * canvas.width / n;
			const y1 = canvas.height * (prices[i] - low) / (high - low);
			const y2 = canvas.height * (prices[i+1] - low) / (high - low);
			line(x1, y1, x2, y2, ctx);
		}
	}

	onMount(async () => {
		const tickers = await apiCall('/api/tickers');
		ticker = tickers[0].ticker;
		const id = tickers[0].id;

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
		{#if ticker}
			<p id="ticker">{ticker}</p>
		{/if}
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

	#ticker {
		padding: 1rem;
	}

	#display {
		border: 1px solid #1f1f1f;		
	}
</style>
