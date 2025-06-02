<script lang="ts">
    import {NavItem,} from 'svelte-ux';
    import {entries} from '@layerstack/utils';
    import {page} from '$app/state';
    import {
        mdiHome,
        mdiProgressClock,
        mdiNoteEdit,
        mdiBankCheck,
        mdiMarkerCheck,
        mdiCloseBoxOutline,
        mdiAccountStar,
        mdiAccountGroup,
        mdiCity,
        mdiFaceAgent,
        mdiTestTube,
        mdiGraph,
        mdiWebSync,
    } from '@mdi/js'; // Icons from Material Design Icons
    import {appBarTitleStore, type MainMenuSegment} from '$lib/stores';

    const RequestsSubMenu: MainMenuSegment[] = [
        {text: "В работе", icon: mdiProgressClock, path: "/BG_req/Progress"},
        {text: "Черновики", icon: mdiNoteEdit, path: "/BG_req/Drafts"},
        {text: "Завершенные", icon: mdiBankCheck, path: "/BG_req/Complete"}
    ]

    const OrganisationsSubMenu: MainMenuSegment[] = [
        {text: "Подтвержденные организации", icon: mdiMarkerCheck, path: "/Organisation/Complete"},
        {text: "Черновики", icon: mdiNoteEdit, path: "/Organisation/Drafts"},
        {text: "Отклоненные", icon: mdiCloseBoxOutline, path: "/Organisation/Rejected"}
    ];

    const BankSubMenu: MainMenuSegment[] = [];


    const ManagerSubMenu: MainMenuSegment[] = [
        {text: "Мои агенты", icon: mdiAccountStar, path: "/Manager/MyAgents"},
        {text: "Агенты моей группы", icon: mdiAccountGroup, path: "/Manager/GroupAgents"},
    ];
    const AgentSubMenu: MainMenuSegment[] = [
        {text: "Мои менеджер", icon: mdiAccountStar, path: "/Agents/Manager"},
    ];
    const GraphSubMenu: MainMenuSegment[] = [
        {text: "Примеры Графиков", icon: mdiGraph, path: "/Sandbox/Graph"},
        {text: "ARC Пример", icon: mdiGraph, path: "/Sandbox/Arc",},
        {text: "Таблицы", icon: mdiGraph, path: "/Sandbox/Tables",},
        {text: "Календарики", icon: mdiGraph, path: "/Sandbox/Dates",},
        {text: "ws песочница", icon: mdiWebSync, path: "/Sandbox/ws-operations",},
    ];

    interface FunctionalMenu {
        MainMenu: MainMenuSegment
        RequestsMenu: MainMenuSegment
        OrganisationMenu: MainMenuSegment
        BankMenu: MainMenuSegment
        ManagerMenu: MainMenuSegment
        AgentMenu: MainMenuSegment
        SandBoxMenu: MainMenuSegment
        PassportMenu: MainMenuSegment
    }

    const MaxFuncMenu: FunctionalMenu = {
        MainMenu: {
            text: "Главная",
            icon: mdiHome,
            path: "/",
        },
        RequestsMenu: {
            text: "Заявки на БГ",
            icon: mdiNoteEdit,
            path: "/BG_req",
            submenu: RequestsSubMenu,
        },
        OrganisationMenu: {
            text: "Организации",
            icon: mdiCity,
            path: "/Organisation",
            submenu: OrganisationsSubMenu,
        },
        BankMenu: {
            text: "Банки",
            icon: mdiCity,
            path: "/Banks",
            submenu: BankSubMenu,
        },
        ManagerMenu: {
            text: "Менеджер",
            icon: mdiCity,
            path: "/Manager",
            submenu: ManagerSubMenu,
        },
        AgentMenu: {
            text: "Агенты",
            icon: mdiFaceAgent,
            path: "/Agents",
            submenu: AgentSubMenu,
        },
        SandBoxMenu: {
            text: "Песочница",
            icon: mdiTestTube,
            path: "/Sandbox",
            submenu: GraphSubMenu,
        },
        PassportMenu: {
            text: "Паспорта",
            icon: mdiTestTube,
            path: "/passports",
        }
    }

    function updateAppBarTitle(newTitleParts: MainMenuSegment[]) {
        appBarTitleStore.set(newTitleParts);
    }
</script>
{#each entries(MaxFuncMenu) as [key, MenuItem]}
    <!--{console.log(MenuItem)} -->
    <!--  #TODO Проверка на разрешение показа меню от бэка -->
    <NavItem text={MenuItem.text} icon={MenuItem.icon} currentUrl={page.url} path={MenuItem.path}
             classes={{ root: "pl-1", active: "bg-primary/10 text-primary" }}
             on:click={() => updateAppBarTitle([MenuItem,])}/>
    {#if MenuItem.submenu}
        {#each MenuItem.submenu as SubMenuItem}
            <!-- {console.log(SubMenuItem)} -->
            <NavItem text={SubMenuItem.text} icon={SubMenuItem.icon} currentUrl={page.url} path={SubMenuItem.path}
                     classes={{ root: "pl-5", active: "bg-primary/10 text-primary-30" }}
                     on:click={() => updateAppBarTitle([MenuItem,SubMenuItem])}/>
        {/each}
    {/if}
{/each}




