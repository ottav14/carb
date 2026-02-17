<script>
	export let value;
	export let items = [];
	let open = false;

	const handleDropButton = () => {
		open = !open;
	}

	const setVal = (val) => {
		value = val;
		open = false;
	}
</script>

<main>
	<li class="itemButton">{value}</li>
	<button on:mousedown={handleDropButton} id="dropButton">
		<svg xmlns="http://www.w3.org/2000/svg" width="32px" height="32px" viewBox="0 -960 960 960" fill="#fff"><path d="M480-360 280-560h400L480-360Z"/></svg>
	</button>
	{#if open}
		<div id="items">
			{#each items as item}
				<button on:mousedown={() => setVal(item)} class="itemButton"><li>{item}</li></button>
			{/each}
		</div>
	{/if}
</main>

<style>
	main {
		display: flex;
		position: relative;
		width: 15rem;
		background-color: #000;
		color: #fff;
		border: 1px solid #1f1f1f;
		list-style: none;
		margin-right: 1rem;
	}

	.item:hover {
		background-color: #1f1f1f;
	}

	#items {
		display: flex;
		flex-direction: column;
		position: absolute;
		top: calc(100% + 1px);
		left: -2px;
		width: 100%;
		border-right: 1px solid #1f1f1f;
		border-left: 1px solid #1f1f1f;
		border-bottom: 1px solid #1f1f1f;
	}

	.itemButton {
		background-color: #000;
		color: #ededed;
		font-size: 24pt;
		border: none;
		padding: 1rem;
		flex-grow: 1;
	}

	.itemButton:hover {
		background-color: #1f1f1f;
	}

	#dropButton {
		background-color: #000;
		height: 100%;
		aspect-ratio: 1 / 1;
		border: none;
		border-left: 1px solid #1f1f1f;
	}

	#dropButton:hover {
		background-color: #1f1f1f;
	}
</style>
