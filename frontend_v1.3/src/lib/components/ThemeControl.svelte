<script lang="ts">
    import {getThemeNames} from "@layerstack/tailwind";
    import themesFileContent from '$lib/themes.json' with {type: 'json'};
    import {ru} from 'date-fns/locale/ru';
    //import {entries, createLocaleSettings} from '@layerstack/utils';
    import {
        ThemeSelect, Tooltip,
    } from 'svelte-ux';
    import {ThemeInit, settings, getSettings} from 'svelte-ux';



</script>
<ThemeInit/>
<Tooltip title="Выбор темы" placement="left" offset={2}>
    <ThemeSelect/>
</Tooltip>
