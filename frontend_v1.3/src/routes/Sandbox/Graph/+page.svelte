<script lang="ts">
    import {
        Arc,
        Chart,
        Group,
        LinearGradient,
        Svg,
        Text,
        Axis,
        Area,
        Points,
        Spline,
        BarChart,
        ClipPath,
    } from 'layerchart';

    import {
        randomNormal,
    } from 'd3-random';

    import {RangeField, Card, SpringValue} from 'svelte-ux';
    import CurveMenuField from '$lib/sandbox/CurveMenuField.svelte';
    import type {ComponentProps} from "svelte";

    let curve = $state();
    let tweened = $state(true);
    const motion = $derived(tweened ? 'tween' : 'none');
    let showLine = $state(true);
    const now = new Date();

    let renderContext = 'canvas';
    let value = $state(75);
    let segments = $state(50);
    let dateRange = $state(10);
    const Context = $state(Svg); //canvas
    let randomCount = $state(1000);
    let random = $state(randomNormal());

    let data = [
        {
            "x": 1,
            "y": 0
        },
        {
            "x": 2,
            "y": 0.8414709848078965
        },
        {
            "x": 3,
            "y": 0.9092974268256817
        },
        {
            "x": 4,
            "y": 0.1411200080598672
        },
        {
            "x": 5,
            "y": -0.7568024953079282
        },
        {
            "x": 6,
            "y": -0.9589242746631385
        },
        {
            "x": 7,
            "y": -0.27941549819892586
        },
        {
            "x": 8,
            "y": 0.6569865987187892
        },
        {
            "x": 9,
            "y": 0.9893582466233818
        },
        {
            "x": 10,
            "y": 0.4121184852417566
        }
    ]
    let data2 = [
        {
            "date": new Date('2025-05-17T21:00:00.000Z'),
            "value": 44,
            "baseline": 62
        },
        {
            "date": new Date('2025-05-18T21:00:00.000Z'),
            "value": 32,
            "baseline": 28
        },
        {
            "date": new Date('2025-05-19T21:00:00.000Z'),
            "value": 40,
            "baseline": 82
        },
        {
            "date": new Date('2025-05-20T21:00:00.000Z'),
            "value": 78,
            "baseline": 50
        },
        {
            "date": new Date('2025-05-21T21:00:00.000Z'),
            "value": 58,
            "baseline": 85
        },
        {
            "date": new Date('2025-05-22T21:00:00.000Z'),
            "value": 39,
            "baseline": 68
        },
        {
            "date": new Date('2025-05-23T21:00:00.000Z'),
            "value": 96,
            "baseline": 78
        },
        {
            "date": new Date('2025-05-24T21:00:00.000Z'),
            "value": 31,
            "baseline": 21
        },
        {
            "date": new Date('2025-05-25T21:00:00.000Z'),
            "value": 75,
            "baseline": 64
        },
        {
            "date": new Date('2025-05-26T21:00:00.000Z'),
            "value": 22,
            "baseline": 93
        }
    ]

    function getRandomDate(from: Date, to: Date) {
        const fromTime = from.getTime();
        const toTime = to.getTime();
        return new Date(fromTime + random() * (toTime - fromTime));
    }


</script>
<svelte:head>
    <title>Примеры графиков</title>
    <meta name="description" content="User profile"/>
</svelte:head>

<div class="text-column prose ">
    <h1>Примеры графиков</h1>
    <div class="mb-2">
        <RangeField label="Value" bind:value/>
        <Card>Не видно число... что-то со стилями</Card>
    </div>
    <div class="h-[220px] p-4 border resize overflow-auto">

        <Chart>
            <Svg center>
                <Group>
                    <LinearGradient class="from-secondary to-primary" let:gradient>
                        <Arc
                                {value}
                                range={[-120, 120]}
                                outerRadius={60}
                                innerRadius={50}
                                cornerRadius={5}
                                motion="spring"
                                fill={gradient}
                                track={{ class: "fill-none stroke-surface-content/10" }}
                        >
                            {#snippet children({value: value})}
                                <Text
                                        value={Math.round(value) + "%"}
                                        textAnchor="middle"
                                        verticalAnchor="middle"
                                        class="text-3xl tabular-nums fill-surface-content"
                                        dominant-baseline="middle"
                                        dy="0.35em"
                                />
                            {/snippet}
                        </Arc>
                    </LinearGradient>
                </Group>
            </Svg>
        </Chart>
    </div>
    <div class="h-[200px] p-4 border resize overflow-auto">
        <Chart>
            <Svg center>
                <Arc
                        value={value*10}
                        domain={[0, 1000]}
                        innerRadius={-20}
                        cornerRadius={10}
                        class="fill-red-500"
                        track={{ class: "fill-red-500/10" }}
                />
                <Arc
                        value={value/3}
                        domain={[0, 30]}
                        outerRadius={-25}
                        innerRadius={-20}
                        cornerRadius={10}
                        class="fill-lime-400"
                        track={{ class: "fill-lime-400/10" }}
                />
                <Arc
                        value={value/10}
                        domain={[0, 12]}
                        outerRadius={-50}
                        innerRadius={-20}
                        cornerRadius={10}
                        class="fill-cyan-400"
                        track={{ class: "fill-cyan-500/10" }}
                />
            </Svg>
        </Chart>
    </div>

    <CurveMenuField bind:value={curve}/>
    <Card>{curve}</Card>
    <div class="h-[300px] p-4 border rounded-sm">
        <Chart {data} x="x" y="y" yNice padding={{ left: 16, bottom: 24 }}>
            <Svg>
                <Axis placement="left" grid rule/>
                <Axis placement="bottom" rule/>
            </Svg>

            <Context>

                <Area

                        {curve}
                        {motion}
                        class="fill-primary/10"
                />

                <Points {motion} r={3} class="fill-surface-100 stroke-primary"/>
            </Context>
        </Chart>
    </div>
    <div class="h-[300px] p-4 border rounded-sm">
        <Chart
                {data}
                x="x"
                y="y"
                yNice
                padding={{ left: 24, bottom: 24, top: 4, right: 8 }}
        >
            <Context>
                <Axis placement="left" grid rule/>
                <Axis placement="bottom" rule/>


                <Spline
                        {curve}
                        motion={motion === "tween" ? "tween" : "none"}
                        draw={motion === "draw"}
                        class="stroke-primary stroke-2"
                />

                <Points
                        motion={motion === "tween" ? "tween" : "none"}
                        r={3}
                        class="fill-surface-100 stroke-primary"
                />
            </Context>
        </Chart>
    </div>
    <div class="h-[300px] p-4 border rounded-sm">
        <BarChart data={data2} x="date" y="value" {renderContext}/>
    </div>
        <div class="grid grid-flow-col gap-3 mb-2">
            <RangeField label="Value" bind:value/>
            <RangeField label="Segments" bind:value={segments} min={2}/>
        </div>
    <div class="h-[240px] p-4 border resize overflow-auto">
        <Chart>
            <Svg center>
                <SpringValue {value} let:value>
                    <ClipPath>
                        <svelte:fragment slot="clip">
                            {#each {length: segments} as _, segmentIndex}
                                {@const segmentAngle = (2 * Math.PI) / segments}
                                <Arc
                                        startAngle={segmentIndex * segmentAngle}
                                        endAngle={(segmentIndex + 1) * segmentAngle}
                                        innerRadius={-20}
                                        cornerRadius={3}
                                        padAngle={0.02}
                                />
                            {/each}
                        </svelte:fragment>
                        <Arc
                                value={value ?? 0}
                                innerRadius={-20}
                                spring
                                class="fill-success-300"
                                track={{ class: "fill-surface-content/10" }}
                        />
                    </ClipPath>

                    <Text
                            value={Math.round(value ?? 0)}
                            textAnchor="middle"
                            verticalAnchor="middle"
                            dy={16}
                            class="text-6xl tabular-nums"
                    />
                </SpringValue>
            </Svg>
        </Chart>
    </div>

</div>

