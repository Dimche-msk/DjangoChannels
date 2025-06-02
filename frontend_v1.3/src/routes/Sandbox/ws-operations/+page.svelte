<script lang="ts">
    import {/*fwStore,*/ wsStore} from '$lib/connections';
    import type {FW2, Ws} from '$lib/fw2-websocket/fw2-ws-classes'; // Для типизации
    import {onMount, onDestroy} from 'svelte';
    import {Button, Card} from "svelte-ux";

    let notify_data_receiver = $state();
    let long_data_receiver = $state("Пока не загружено ничего");
    let notify1 = $state("Пока нет данных");
    let pasports_data_receiver = $state();

    let loading_state = $state(false)


    const currentWsInstance = $wsStore; // Получаем значение напрямую


    onMount(() => {
        currentWsInstance.call('ws/notify', {}, true)

        currentWsInstance.notify.addEventListener('notify1', async function (e) {
            notify1 = e.detail
            console.log('notify1', params)
        })
    });

    onDestroy(() => {
        // Здесь грохаем все зависшие RPC, если надо
    });

    async function long_ws() {
        loading_state = true
        console.warn("Дергам WS  long")
        long_data_receiver = await currentWsInstance.call('ws/long', 22)
        loading_state = false
    }


    let title = "WS песочница";
</script>

<svelte:head>
    <title>{title}</title>
    <meta name="description" content="main page"/>
</svelte:head>
<h1>WS песочница ('ws/long', 22)</h1>
    <div class="prose lg:prose-xl mx-auto sm:prose-p grid grid-cols-2 gap-3">
        <div>
            <Button variant="fill" color="primary" on:click={long_ws} loading={loading_state} >Дернуть WS</Button>
        </div>
        <div>
            <Card>{long_data_receiver}</Card>
        </div>
    </div>
    <h1>WS песочница ('ws/notify1')</h1>
        <div class="prose lg:prose-xl mx-auto sm:prose-p grid grid-cols-2 gap-3">
            <div>
                <Card>"notify1"</Card>
            </div>
            <div>
                <Card>{notify1}</Card>
            </div>
        </div>

        <style>

        </style>
