<script lang="ts">
    import {Tabs} from 'svelte-ux';


    let options = [
        {label: 'One', value: 1},
        {label: 'Two', value: 2},
        {label: 'Three', value: 3},
        {label: 'Four', value: 4},
    ];
    let value = $state(0);

</script>

<svelte:head>
    <title>About</title>
    <meta name="description" content="About this app"/>
</svelte:head>
<Tabs {options} placement="top" bind:value classes={{content:  " bg-surface-200 border px-4 py-2 rounded-b rounded-tr", tab: { root: "rounded-t ", },}}>
    <svelte:fragment slot="content" let:value>
        Page {value}

        <div class="text-column">
            <h1>About this app</h1>

            <p>
                This is a <a href="https://svelte.dev/docs/kit">SvelteKit</a> app. You can make your own by typing
                the following into your command line and following the prompts:
            </p>

            <pre>npx sv create</pre>

            <p>
                The page you're looking at is purely static HTML, with no client-side interactivity needed.
                Because of that, we don't need to load any JavaScript. Try viewing the page's source, or opening
                the devtools network panel and reloading.
            </p>

        </div>


    </svelte:fragment>
</Tabs>
