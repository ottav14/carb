<script>
	import Panel from './components/Panel.svelte';
	import Button from './components/Button.svelte';

	let panels = [];

	const addPanel = () => {
		panels = [...panels, Panel];
	}

</script>

<main>
	<div id="container">
		{#each panels as panel, i}
			<svelte:component this={panel} />
		{/each}
		<Button type="add" onclick={addPanel} />
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

	#container {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 80%;
		height: 80%;
	}
</style>
