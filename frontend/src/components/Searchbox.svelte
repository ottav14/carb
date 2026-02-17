<script>
import { createEventDispatcher } from "svelte";

export let suggestions = [];
export let placeholder;
	
let open = false;
let query;
const dispatch = createEventDispatcher();

const setVal = (val, e) => {
	query = val;
	open = false;
	dispatch('mousedown', e);
}

const inputFocus = (e) => {
	open = true;
	e.target.select();
}

const inputChange = (e) => {
	query = query.toUpperCase();
	dispatch('input', e);
}
</script>

<main>
	<input 
		type="text" 
		bind:value={query} 
		placeholder={placeholder}
		on:focus={(e) => inputFocus(e)}
		on:input={(e) => inputChange(e)}
	/>
	{#if open}
		<ul class="autocomplete">
			{#each suggestions as s}
				<button on:mousedown={(e) => setVal(s, e)}>
					<li class="suggestion">
						{s}
					</li>
				</button>
			{/each}
		</ul>
	{/if}
</main>
<style>
	input {
		height: 2rem;
		font-size: 24pt;
		border-radius: 0;
		border: 1px solid #1f1f1f;
		background-color: #000;
		color: #ededed;
		padding: 1rem;
		width: 15rem;
	}

	input:focus {
		outline: none;
		box-shadow: none;
		border: 1px solid #ededed;
	}

	input::selection {
		background: #ededed;
		color: #000;
	}

	.autocomplete {
		position: absolute;
		display: flex;
		flex-direction: column;
		top: 100%;
		list-style: none;
		background-color: #000;
		padding: 0;
		border-right: 1px solid #1f1f1f;
		border-left: 1px solid #1f1f1f;
		border-bottom: 1px solid #1f1f1f;
	}

	.suggestion {
		width: 15rem;
		padding: 1rem;
	}

	.suggestion:hover {
		background-color: #1f1f1f;
	}

	button {
		background-color: #000;
		color: #ededed;
		width: 100%;
		padding: 0;
		font-size: 24pt;
		border: none;
	}

	button:focus-visible {
		outline: none;
		box-shadow: none;
		background-color: #ededed;
		color: #000;
	}

</style>
