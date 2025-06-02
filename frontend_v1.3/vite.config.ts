import {sveltekit} from '@sveltejs/kit/vite';
import {defineConfig} from 'vite';
import {resolve} from "path";
import dsv from '@rollup/plugin-dsv';
import {autoType} from 'd3-dsv';

/** @type {import('vite').UserConfig} */
const config = {
    // @ts-expect-error
    plugins: [sveltekit(), /*sveld(),*/ dsv({processRow: autoType})],
    // optimizeDeps: {
    //   include: ['svelte-ux'],
    // },
    server: {
        host: '0.0.0.0',
        port: 5173, // Основной порт. Если запускать одновременно, нужен другой порт для одного из них.
        proxy: {
            '/ws': {
                target: 'ws://localhost:8000',
                changeOrigin: true,
                ws: true,
            },
            '/login': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                ws: false,
            },
            '/admin': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                ws: false,
            },

        },
    },
    resolve: {
        alias: {
            '$lib': resolve(__dirname, 'src/lib')
        }
    },
};
export default config;