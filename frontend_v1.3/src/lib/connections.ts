// src/lib/connections.ts
import { writable, readable, type Writable, type Readable } from 'svelte/store';
import { FW2, Ws } from '$lib/fw2-websocket/fw2-ws-classes';


const currentProductionFlag = false;

// const fwInstance = new FW2('ws', 0, currentProductionFlag);
const wsInstance = new Ws(undefined, currentProductionFlag);


// 3. Создание Svelte stores
// Для FW2, который имеет асинхронную инициализацию
export const fwStore: Writable<FW2 | null> = writable(null);

// Для Ws, если у него нет асинхронной инициализации, можно использовать readable
// Если Ws также требует асинхронной инициализации, используйте writable(null) по аналогии с fwStore
export const wsStore: Readable<Ws> = readable(wsInstance);

// 4. Функция для инициализации FW2 (и других сервисов, если нужно)
//export async function initializeConnections(): Promise<void> {
//    try {
//        await fwInstance.init(); // Вызываем асинхронный init
//        fwStore.set(fwInstance); // Обновляем store с инициализированным экземпляром
//        console.log('FW2 connection initialized and ready.');
//
//        // Если wsInstance также требует асинхронной инициализации:
//        // await wsInstance.init();
//        // wsStore.set(wsInstance); // (если wsStore был writable)
//        // console.log('Ws connection initialized and ready.');
//
//    } catch (error) {
//        console.error('Failed to initialize connections:', error);
//        // Здесь можно обработать ошибки инициализации, возможно, установить store в состояние ошибки
//        fwStore.set(null); // или специальный объект ошибки
//    }
//}