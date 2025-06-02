<script lang="ts">
    import '../app.css';

    import { onMount } from 'svelte';
    import { /*initializeConnections,*/ /*fwStore,*/ wsStore, } from '$lib/connections';


    import HeaderComponent from '../lib/Header.svelte';
    import NavMenuComponent from '../lib/NavMenu.svelte';
    import {AppBar, AppLayout, Button, getSettings, Icon, settings} from "svelte-ux";
    import {mdiMicrosoftXboxControllerMenu,} from '@mdi/js'
    import {appBarTitleStore, type MainMenuSegment} from '$lib/stores';
    import {goto} from "$app/navigation";
    import {page} from '$app/state';
    import {ru} from 'date-fns/locale/ru';
    import {ruDictionary} from '$lib/ruDictionary';
    import allThemes from '$lib/themes.json';
    import {createLocaleSettings} from "@layerstack/utils";

    let {children} = $props();


    onMount(async () => {

        //await initializeConnections();

        // Пример подписки на store для отладки или реакции в макете
        // const unsubscribeFw = fwStore.subscribe(fwInstance => {
        //     if (fwInstance) {
        //         console.log('FW instance is now available in layout:', fwInstance);
        //         // Здесь можно, например, подписаться на события от fwInstance.notify
        //         // fwInstance.notify.addEventListener('someEvent', (e) => console.log(e));
        //     } else {
        //         console.log('FW instance is not yet available or failed to initialize.');
        //     }
        // });

        // Не забудьте отписаться, если макет может быть уничтожен (для корневого это редкость)
        // return () => {
        //     unsubscribeFw();
        // };
    });



    const lightThemes: string[] = [];
    const darkThemes: string[] = [];

    for (const themeName in allThemes) {
        if (Object.hasOwnProperty.call(allThemes, themeName)) {
            // @ts-ignore // Может понадобиться для доступа по индексу к импортированному JSON
            const themeDetails = allThemes[themeName];
            if (themeDetails['color-scheme'] === 'light') {
                lightThemes.push(themeName);
            } else if (themeDetails['color-scheme'] === 'dark') {
                darkThemes.push(themeName);
            }
        }
    }

    const russianLocaleSettings = createLocaleSettings({
        locale: "ru",
        dictionary: ruDictionary,
        formats: { /* ... */}
    });


    settings({
        themes: {
            light: lightThemes,
            dark: darkThemes,
        },
         locales: {
            ru: ru,
        },
        localeFormats: {
            ru: russianLocaleSettings
        },
        fallbackLocale: 'ru', // Локаль по умолчанию
    });


    const sx = getSettings();
    if (sx && sx.locale && typeof sx.locale.set === 'function') {
        sx.locale.set("ru");
        console.log('+layout.svelte: svelte-ux locale explicitly set to "ru"');
    } else {
        console.warn('+layout.svelte: Не удалось явно установить локаль через getSettings().locale.set("ru")');
    }

</script>

<AppLayout>
    <AppBar menuIcon={mdiMicrosoftXboxControllerMenu}
            class="bg-primary-600 text-primary-content">
        {#each $appBarTitleStore as MenuItem}
            <Button variant="fill-light" color="primary"
                    class="p-1.5 rounded-full hover:bg-white/10"
                    on:click={() => {
                         if (page.url.pathname !== MenuItem.path) // dont update if the same page
                        {
                            appBarTitleStore.set([MenuItem, ]);
                            goto(MenuItem.path);
                        }
                    }}
                    aria-label={MenuItem.text || 'Перейти в раздел'}
            >
                <Icon data={MenuItem.icon} class="text-xl"/>{MenuItem.text}
            </Button>
            >
        {/each}
        <div slot="actions">
            <HeaderComponent/>
        </div>
    </AppBar>
    <svelte:fragment slot="nav">
        <NavMenuComponent/>
    </svelte:fragment>
    <main>
        {@render children()}
    </main>
</AppLayout>

<style>
    /*
      Меню-бар (слева) - делаем, что бы не просвечивал
    */
    :global(aside.fixed) {
        background-color: hsl(var(--color-surface-300));
        opacity: 1 !important;
    }
</style>