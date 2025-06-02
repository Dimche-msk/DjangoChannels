import {writable} from 'svelte/store';
import {mdiHome,} from '@mdi/js';

//Строка навигации в Хедере
export interface MainMenuSegment {
    text: string;      // Текст сегмента (может быть aria-label для иконки)
    icon?: string;      // Путь к иконке MDI (например, mdiHome)
    path: string;      // URL для навигации при клике
    submenu?: MainMenuSegment[]; // Подменю
}
export const appBarTitleStore = writable<MainMenuSegment[]>([{text: 'Главная страница', icon:mdiHome, path:"/"},]);
