<script lang="ts">
    import {DatePickerField, DateRange, Shine, DateRangeField, Duration, Card} from 'svelte-ux';
    import {PeriodType, getDateFuncsByPeriodType} from '@layerstack/utils';
    import {set, subDays, addMilliseconds} from 'date-fns';


    let value = $state(0);

    interface DateInterval {
        from: Date,
        to: Date
    }


    const today = new Date();
    const yesterday = subDays(today, 1);


    let date_interval: DateInterval = $state({
        from: set(subDays(today, -1), {hours: 0, minutes: 0, seconds: 0, milliseconds: 0}), // Начало вчерашнего дня
        to: set(subDays(today, -366), {hours: 0, minutes: 0, seconds: 0, milliseconds: 0})    // Конец сегодняшнего дня
    });

    // Ловим события изменения интервала не зависимо от элементов выбора
    $effect(() => {
        console.debug("date_interval change (snapshot):", $state.snapshot(date_interval));
    })

    // функция обработки изменения интервала
    function handleIntervalChange(e: any) {
        console.debug('on:change', e);
        date_interval = e.detail;


    }
</script>

<h1>Маленькая выбиралка интервала (с сиянием :)) Не вызывает варнингов в консоли и не откликается на изменение</h1>

<Shine depth={1} lightColor="#FF0000">
    <h1>DateRange: {date_interval.from.toDateString()}- {date_interval.to.toDateString()}</h1>
    <DateRangeField
            value={{
        from: set(yesterday, { hours: 0, minutes: 0, seconds: 0, milliseconds: 0 }), // Начало вчерашнего дня
        to: set(today, { hours: 23, minutes: 59, seconds: 59, milliseconds: 999})    // Конец сегодняшнего дня
    }}
            periodTypes={[PeriodType.Day]}
            on:change={handleIntervalChange}

    />
</Shine>
<h1>Маленькая выбиралка интервала (с сиянием :)) Вызывает варнинги в консоли и откликается на изменение #TODO
    разобраться с пропсами и биндами</h1>

<Shine depth={1} lightColor="#FF0000">
    <h1>DateRange: {date_interval.from.toDateString()}- {date_interval.to.toDateString()}</h1>
    <DateRangeField

            periodTypes={[PeriodType.Day]}
            bind:value={date_interval}

    />
</Shine>
<div class="grid grid-cols-3 gap-3 ">
    <Card title="Продолжительность" subheading="Действия БГ" class="bg-success/10">
        <div slot="contents" class="flex items-center justify-center">
            <Duration start={date_interval.from}
                      end={date_interval.to.getMilliseconds()===999?addMilliseconds(date_interval.to, 1):date_interval.to}/>
        </div>
    </Card>
</div>

<h1>Большая выбиралка интервала без кнопки ОК
</h1>
<DateRange
        bind:selected={date_interval}
        periodTypes={[PeriodType.Day]}
        getPeriodTypePresets={() => []}

/>



