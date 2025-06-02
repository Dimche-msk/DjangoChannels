<script lang="ts">
    import {Table, Paginate, Pagination} from 'svelte-ux';

    import {cls} from '@layerstack/tailwind';
    import {
        tableCell,
        type ColumnDef,
        getCellValue,
        getCellHeader,
        getHeaders,
        getRowColumns,
        tableOrderStore,
    } from '@layerstack/svelte-table';

    const data = [
        {id: 1, name: 'Cupcake', calories: 305, fat: 3.7, carbs: 67, protein: 4.3},
        {id: 2, name: 'Donut', calories: 452, fat: 25.0, carbs: 51, protein: 4.9},
        {id: 3, name: 'Eclair', calories: 262, fat: 16.0, carbs: 24, protein: 6.0},
        {id: 4, name: 'Frozen yogurt', calories: 159, fat: 6.0, carbs: 24, protein: 4.0},
        {id: 5, name: 'Gingerbread', calories: 356, fat: 16.0, carbs: 49, protein: 3.9},
        {id: 6, name: 'Honeycomb', calories: 408, fat: 3.2, carbs: 87, protein: 6.5},
        {id: 7, name: 'Ice cream sandwich', calories: 237, fat: 9.0, carbs: 37, protein: 4.3},
        {id: 8, name: 'Jelly Bean', calories: 375, fat: 0.0, carbs: 94, protein: 0.0},
        {id: 9, name: 'KitKat', calories: 518, fat: 26.0, carbs: 65, protein: 7.0},
        {id: 10, name: 'Lollipop', calories: 392, fat: 0.2, carbs: 98, protein: 0.0},
        {id: 11, name: 'Marshmallow', calories: 318, fat: 0.0, carbs: 81, protein: 2.0},
        {id: 12, name: 'Nougat', calories: 360, fat: 19.0, carbs: 9, protein: 37.0},
        {id: 13, name: 'Oreo', calories: 437, fat: 18.0, carbs: 63, protein: 4.0},
    ];

    const order = tableOrderStore({initialBy: 'calories', initialDirection: 'desc'});


    console.log(order);
</script>
<div class="container mx-auto box-border">
    <h1> Табличка с сортировкой, пагинацией и диаграмкой</h1>
    <Paginate {data} perPage={5} let:pageData let:pagination>
        <Table class=""
               data={[...pageData].sort($order.handler)}
               columns={[
    {
      name: "name",
      align: "left",
      classes: {
        td: "from-primary/5 to-primary/10 ",
      },
    },
    {
      name: "calories",
      align: "center",
      format: "integer",
       dataBackground: {
        inset: [1, 2],
        tweened: { duration: 300 },
      },
      classes: {
        td: "from-primary/5 to-primary/30 ",
      },
    },
    {
      name: "fat",
      align: "right",
      format: "integer",
    },
    {
      name: "carbs",
      align: "right",
      format: "integer",
    },
    {
      name: "protein",
      align: "right",
      format: "integer",
    },
  ]}
               {order}
               classes={{
                // ----------------Стилизация через классы Tailwind -------------------------
                table: 'min-w-full divide-y divide-surface-300', // Общие классы для таблицы
                thead: '', // Классы для <thead>, если нужно
                tbody: 'divide-y divide-surface-200 bg-surface-100', // Классы для <tbody>
                tr: '', // Классы для <tr>
                th: 'px-4 py-3 text-center text-xs font-medium uppercase tracking-wider bg-surface-200 text-surface-content font-bold text-lg', // Стили для всех <th>
                // ^^^^ Изменения здесь:
                // bg-surface-200 (или bg-surface-300 для еще более темного, если surface-200 - это фон страницы)
                // text-surface-content (для цвета текста, чтобы обеспечить контраст)
                // font-bold (жирный шрифт)
                // text-lg (увеличенный размер шрифта, можно text-xl для еще большего)
                // px-4 py-3 (пример отступов, настройте по вкусу)
                // text-left (выравнивание текста, можно изменить на text-center или text-right)
                td: 'px-4 py-3 whitespace-nowrap', // Общие классы для <td>
            }}
        />
        <Pagination
                {pagination}
                perPageOptions={[5, 10, 25, 100]}
                show={["perPage", "pagination", "prevPage", "nextPage"]}
                classes={{
      root: "border-t py-1 mt-2",
      perPage: "flex-1 text-right",
      pagination: "px-8",
    }}
        />
    </Paginate>
</div>
