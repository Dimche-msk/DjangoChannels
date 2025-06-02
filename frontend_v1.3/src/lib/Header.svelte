<script lang="ts">
    import {page} from '$app/state';
    import ThemeControl from "$lib/components/ThemeControl.svelte";
    import {mdiAccountCircleOutline, mdiLogout, mdiMenuDown} from '@mdi/js';
    import {Button, ButtonGroup, Tooltip, Toggle, Menu, MenuItem} from "svelte-ux";
    import {lgScreen} from '@layerstack/svelte-stores';

</script>

<header>
    <div class="corner-actions">
        {#if $lgScreen}
            <Tooltip title="Профиль" placement="left" offset={2}>
                <Button
                        icon={mdiAccountCircleOutline}
                        href="/Profile"
                        class="p-2"
                        aria-label="Profile"
                />
            </Tooltip>
            <Tooltip title="Выход из системы" placement="left" offset={2}>
                <Button
                        icon={mdiLogout}
                        href="/LogOut"
                        class="p-2"
                        aria-label="Profile"
                />
            </Tooltip>
            <ThemeControl/>
        {:else}
            <div class="grid gap-2">
                <ButtonGroup>
                    <Toggle let:on={open} let:toggle let:toggleOff>
                        <Button icon={mdiMenuDown} on:click={toggle}/>
                        <span>
                            <Menu {open} on:close={toggleOff} placement="bottom-start">
                                <MenuItem>
                                    <Tooltip title="Профиль" placement="left" offset={2}>
                                    <Button
                                            icon={mdiAccountCircleOutline}
                                            href="/Profile/"
                                            class="p-2"
                                            aria-label="Profile"
                                    />
                                    </Tooltip>
                                </MenuItem>
                                <MenuItem>
                                    <Tooltip title="Выход из системы" placement="left" offset={2}>
                                        <Button
                                                icon={mdiLogout}
                                                href="/LogOut/"
                                                class="p-2"
                                                aria-label="Logout"
                                        />
                                    </Tooltip>
                                </MenuItem>
                                 <MenuItem>
                                     <!-- on:click|stopPropagation on:keydown|stopPropagation -->
                                     <div role="group"
                                          aria-label="Настройки темы">
                                        <ThemeControl/>
                                    </div>
                                </MenuItem>
                            </Menu>
                        </span>
                    </Toggle>
                </ButtonGroup>
            </div>
        {/if}

    </div>
</header>

<style>
    header {
        display: flex;
        justify-content: space-between;
        align-items: center; /* Добавлено для вертикального выравнивания по центру */
        padding: 0.5rem 1rem; /* Добавлены небольшие отступы для шапки */
    }


    .corner-actions {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>