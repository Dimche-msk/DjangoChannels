<script lang="ts">
    import {Button, Toggle, Grid, Badge, Progress, Card} from 'svelte-ux';
    import {cls} from '@layerstack/tailwind';

    let size: 'sm' | 'md' | 'lg' = 'md';

    const variants = ['default', 'outline', 'fill', 'fill-light', 'fill-outline', 'text'] as const;
    let badge = $state(10)
    let value = $state(100)
</script>
<svelte:head>
    <title>About</title>
    <meta name="description" content="Песочница"/>
</svelte:head>


<h1> Наша песочница</h1>
<h1>Examples</h1>


<Grid columns={4} gap={8}>
    <div class="mt-2 border">
        <h2>Basic</h2>
        <Badge value={badge} small>
            <Button on:click={() => alert('Why did you do that?')}>Click me 123</Button>
        </Badge>
        <Button loading>Loading...</Button>
        <Badge value={badge} small>
            <Button variant="outline" color="primary" loading>Loading...</Button>
        </Badge>
        <Button variant="fill" color="primary" loading>Loading...</Button>
        <Button variant="fill-light" color="primary" loading>Loading...</Button>
        <Button variant="fill-outline" color="primary" loading>Loading...</Button>
        <Button variant="text" color="primary" loading>Loading...</Button>
    </div>
    <div class="mt-2 border">
        <h2>Загрузка</h2>
        <Toggle let:on={loading} let:toggle>
            <Button {loading} on:click={toggle}>Click me</Button>
        </Toggle>
        <Toggle let:on={loading} let:toggle>
            <Button variant="outline" color="primary" {loading} on:click={toggle}
            >Click me
            </Button
            >
        </Toggle>
        <Toggle let:on={loading} let:toggle>
            <Button variant="fill" color="primary" {loading} on:click={toggle}
            >Click me
            </Button
            >
        </Toggle>
        <Toggle let:on={loading} let:toggle>
            <Button variant="fill-light" color="primary" {loading} on:click={toggle}
            >Click me
            </Button
            >
        </Toggle>
        <Toggle let:on={loading} let:toggle>
            <Button variant="fill-outline" color="primary" {loading} on:click={toggle}
            >Click me
            </Button
            >
        </Toggle>
        <Toggle let:on={loading} let:toggle>
            <Button variant="text" color="primary" {loading} on:click={toggle}
            >Click me
            </Button
            >
        </Toggle>
    </div>


    {#each variants as variant}
        <div class="border">
            <div class="font-semibold my-2"><h2>{variant}</h2></div>
            <div class="grid gap-2 ml-4">
                <!-- Theme colors -->

                <div>
                    <Button {variant} {size}>Default</Button>
                    <Button {variant} {size} color="primary">Primary</Button>
                    <Button {variant} {size} color="secondary">Secondary</Button>
                    <Button {variant} {size} color="accent">Accent</Button>
                    <Button {variant} {size} color="neutral">Neutral</Button>
                </div>
                <div>
                    <!-- State colors -->
                    <Button {variant} {size} color="info">Info</Button>
                    <Button {variant} {size} color="success">Success</Button>
                    <Button {variant} {size} color="warning">Warning</Button>
                    <Button {variant} {size} color="danger">Danger</Button>
                </div>
                <div>
                    <!-- TODO: CSS variables for each variant -->
                    <!-- <Button {variant} {size} class="[--bg-color:theme(colors.blue.500)] [--text-color:white]">
                        Color Variables
                      </Button>
                      <Button {variant} {size} class="[--bg-color:theme(colors.emerald.500)] [--text-color:white]">
                        Color Variables
                      </Button> -->
                </div>
            </div>
        </div>
    {/each}


    <div class="border">
        <Button variant="outline" color="primary">default</Button>
        <Button variant="outline" color="primary" rounded>rounded</Button>
        <Button variant="outline" color="primary" rounded="full">full</Button>
        <Button variant="outline" color="primary" rounded={false}>false</Button>
    </div>
    <div class="border">
        <Button variant="fill" color="primary">default</Button>
        <Button variant="fill" color="primary" rounded>rounded</Button>
        <Button variant="fill" color="primary" rounded="full">full</Button>
        <Button variant="fill" color="primary" rounded={false}>false</Button>
    </div>
    <div class="border">
        <Button variant="fill-light" color="primary">default</Button>
        <Button variant="fill-light" color="primary" rounded>rounded</Button>
        <Button variant="fill-light" color="primary" rounded="full">full</Button>
        <Button variant="fill-light" color="primary" rounded={false}>false</Button>
    </div>
    <div class="border">
        <Button variant="fill-outline" color="primary">default</Button>
        <Button variant="fill-outline" color="primary" rounded>rounded</Button>
        <Button variant="fill-outline" color="primary" rounded="full">full</Button>
        <Button variant="fill-outline" color="primary" rounded={false}>false</Button>
    </div>
    <div class="border">
        <Button class="uppercase">default</Button>
        <Button class="uppercase" variant="outline" color="primary">outline</Button>
        <Button class="uppercase" variant="fill" color="primary">fill</Button>
        <Button class="uppercase" variant="fill-light" color="primary">fill-light</Button>
        <Button class="uppercase" variant="fill-outline" color="primary">fill-outline</Button>
        <Button class="uppercase" variant="text" color="primary">text</Button>
    </div>
    <div class="border">
        <Progress
                bind:value
                class={cls(
    value > 90
      ? "[--color:theme(colors.danger)]"
      : value > 50
        ? "[--color:theme(colors.warning)]"
        : "[--color:theme(colors.success)]",
  )}
                max={100}
        />
        <Card> Движок</Card>
        <input type="range" bind:value class="w-full"/>
    </div>
</Grid>
