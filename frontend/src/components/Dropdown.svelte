<script>
	export let value;
	export let items = [];
</script>

<main>
	<div id="top">
		<li class="item" id="selected">{value}</li>
		<button>
			<svg xmlns="http://www.w3.org/2000/svg" width="32px" height="32px" viewBox="0 -960 960 960" fill="#fff"><path d="M480-360 280-560h400L480-360Z"/></svg>
		</button>
	</div>
	<div id="items">
		{#each items as item}
			<li class="item">{item}</li>
		{/each}
	</div>
</main>

<style>
	main {
		position: relative;
		width: 15rem;
		height: 4rem;
		background-color: #000;
		color: #fff;
		border: 1px solid #1f1f1f;
		list-style: none;
		margin-right: 1rem;
	}

	#top {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		height: 100%;
	}

	.item {
		padding: 1rem;
	}

	.item:hover {
		background-color: #1f1f1f;
	}

	#items {
		position: absolute;
		left: -2px;
		width: 100%;
		border-right: 1px solid #1f1f1f;
		border-left: 1px solid #1f1f1f;
		border-bottom: 1px solid #1f1f1f;
	}

	#selected {
		flex-grow: 1;
	}

	button {
		background-color: #000;
		height: 100%;
		aspect-ratio: 1 / 1;
		border: none;
		border-left: 1px solid #1f1f1f;
	}

	button:hover {
		background-color: #1f1f1f;
	}
</style>
