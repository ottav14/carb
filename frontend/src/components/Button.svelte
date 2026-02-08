<script>
	export let type;
	export let onclick;
</script>

<main>
	<button on:click={onclick}>
		<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#fff"><path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/></svg>
	</button>
</main>

<style>
	main {
	}

	button {
		display: flex;
		justify-content: center;
		align-items: center;
		aspect-ratio: 1 / 1;
		width: 4rem;
		padding: 0;
		font-size: 32pt;
		text-align: center;
		background-color: #000;
		border: 1px solid #1f1f1f;
	}

	button:hover {
		border: 1px solid #ededed;
	}

	button:active {
		background-color: #777;
		transform: scale(0.95);
	}

	button:focus-visible {
		outline: none;
		box-shadow: none;
		background-color: #ededed;
		color: #000;
	}

</style>


