<script lang="ts">
    import {Button, Card} from 'svelte-ux'

    let loading_user_info = $state(false)

    interface User {
        id: bigint | null,
        first_name: string | null,
        last_name: string | null,
        email: string | null,
    }

    let user: User = $state({id: null, first_name: null, last_name: null, email: null})
    let wsError = $state<string | null>(null);

    // Функция для подключения к WebSocket и получения данных
    async function fetchUserInfo() {
        loading_user_info = true;
        wsError = null;
        user = {id: null, first_name: null, last_name: null, email: null}; // Сбрасываем пользователя перед новым запросом

        // Определяем URL для WebSocket.
        // Если Vite dev server запущен, он будет проксировать этот запрос.
        // В продакшене нужно будет настроить веб-сервер (Nginx) для проксирования.
        // Используем относительный путь, чтобы Vite мог его перехватить.
        // Префикс 'ws/' добавляется, если он есть в Django routing и Vite proxy.
        const wsUrl = `ws://${window.location.host}/ws/api/get-user-info/`;
        // Если в Django и Vite нет префикса 'ws/', то:
        // const wsUrl = `ws://${window.location.host}/api/get-user-info/`;


        console.log(`Connecting to WebSocket: ${wsUrl}`);
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            console.log('WebSocket connection established');
            // Консьюмер GetUserInfo отправляет данные сразу после подключения,
            // поэтому здесь мы не отправляем никаких сообщений.
        };

        socket.onmessage = (event) => {
            console.log('Message from server:', event.data);
            try {
                const data = JSON.parse(event.data);
                if (data.message) { // Наш консьюмер отправляет данные в поле "message"
                    user.id = data.message.id;
                    user.first_name = data.message.first_name;
                    user.last_name = data.message.last_name;
                    user.email = data.message.email;
                    wsError = null;
                } else if (data.error) {
                    console.error('Server error:', data.error);
                    wsError = data.error;
                } else {
                    // Неожиданный формат данных
                    console.warn('Received unexpected data format:', data);
                    wsError = 'Получен неожиданный формат данных от сервера.';
                }
            } catch (e) {
                console.error('Failed to parse JSON from server:', e);
                wsError = 'Ошибка при обработке ответа от сервера.';
            }
            loading_user_info = false;
            // socket.close(); // Консьюмер сам закрывает соединение, но можно и здесь
        };

        socket.onerror = (error) => {
            console.error('WebSocket Error:', error);
            wsError = 'Ошибка WebSocket соединения.';
            loading_user_info = false;
        };

        socket.onclose = (event) => {
            console.log('WebSocket connection closed:', event.code, event.reason);
            if (!user.id && !wsError) { // Если соединение закрылось без данных и без явной ошибки
                // wsError = 'Соединение закрыто сервером без передачи данных.';
            }
            loading_user_info = false;
        };
    }
</script>
<svelte:head>
    <title>Банковские гарантии</title>
    <meta name="description" content="main page"/>
</svelte:head>
<h1>Главная страница</h1>



<Button loading={loading_user_info} on:click={fetchUserInfo} variant="fill-light" color="primary">get User Info</Button>

<Card title="User ID">{user.id}</Card>
<Card title="User name">{user.first_name}</Card>
<Card title="User name">{user.last_name}</Card>
<Card title="User email">{user.email}</Card>



<style>

</style>
