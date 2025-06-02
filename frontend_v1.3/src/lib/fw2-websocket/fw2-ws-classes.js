class fw2fn {

    static init() {
        const _this = this
    }

    static id_to_int(str) { // covert str "aaa123" or int to int 123
        if (Number.isInteger(str)) {
            return str
        }
        let numb = str.match(/(\d)+/g)
        try {
            return parseInt(numb[numb.length - 1], 10);
        } catch {
            return null;
        }
    }

    static id_to_arr_int(d) { // covert str or [str1, str2] to int array
        if (!Array.isArray(d)) {
            d = [d]
        }
        let ret = []
        for (let item of d) {
            let int_item = this.id_to_int(item)
            if (int_item !== null) {
                ret.push(int_item)
            }
        }
        return ret
    }
}


class FW2 {
    static on_close_ws() {
        let src = "static/pic/disconnected-16.svg"
        this._connect_f = false
        document.body.innerHTML = `<div class="h-100 d-flex align-items-center justify-content-center">
    <div><img src="${src}" style="width: 8rem" class="card-img-top pe-4" alt=""></div>
    <div>
        <h5 class="pb-2">Сессия закрыта</h5>
        <a href="#" class="btn btn-primary" onclick="location.reload()">Новая сессия</a>
    </div>
</div>`
    }

    constructor(url, keepalive = 0, wss = false, token) {
        const _this = this
        this._url = url
        this._keepalive(keepalive)
        this._wss = wss
        this._token = token
        console.log('this._token', this._token)
        // RPC
        this.notify = new EventTarget();
        this._rpc_id = 0
        this._receive_rpc_fn_dict = {}  // {rpc_id: fn}
        // Global vars
        this._ws_id = null
        this._connect_f = false
        // Public functions
        this.get_table = async function (...args) {
            return await _this._get_table(...args)
        }
        // on close browser
        window.onbeforeunload = function () {
            _this._ws.send('close');
        }
        this._ping(0)
    }

    async init() {
        const _this = this
        let protocol = 'ws'
        if (this._wss) protocol = 'wss'
        console.log('this._token', this._token)
        console.log('this._url', this._url)
        if (this._token.length > 1) {
            this._token = `?token=${this._token}`
        }
        this._ws = new WebSocket(`${protocol}://${location.hostname}:${location.port}/${this._url}${this._token}`)
        this._ws.onopen = () => {
            this._connect_f = true
        }
        this._ws.onmessage = (m) => {
            this._receive_rpc(m)
        }

        this._ws.onclose = () => {
            this.on_close_ws()
        }
    }

    _receive_rpc(m) {
        let msg = JSON.parse(m.data)
        if (msg.jsonrpc !== '2.0') return false
        if (msg.method) {  // this is Notify
            this.notify.dispatchEvent(new CustomEvent(msg.method, {detail: msg.params}))
        } else {
            if (msg.id > 0) {
                let err = false
                if (msg.error) {
                    err = msg.error
                }
                this._receive_rpc_fn_dict[msg.id](msg.result, err) // todo send error
            }
        }
    }

    call_rpc(rpc_name, params = {}, error = true) {
        const _this = this
        return new Promise((resolve, reject) => {
            if (!this._connect_f) {
                if (error) {
                    reject('ws not connected')
                } else {
                    resolve(false)
                }
            }
            this._rpc_id++;
            const rpc_id = this._rpc_id
            let rpc = JSON.stringify({jsonrpc: "2.0", method: rpc_name, "params": params, "id": rpc_id})
            this._ws.send(rpc)
            this._receive_rpc_fn_dict[rpc_id] = (d, err) => {
                if (!err) {
                    resolve(d)
                } else {
                    if (error) {
                        reject(err)
                    } else {
                        resolve(false)
                    }
                }
                delete _this._receive_rpc_fn_dict[rpc_id]
                // console.log('_receive_rpc_fn_dict', _this._receive_rpc_fn_dict)
            }
        })
    }

    get ws_id() {
        return this._ws_id
    }

    get token() {
        return this._token
    }

    _keepalive(interval) {
        if (interval > 0) {
            setInterval(async function f() {
                await fetch('/keepalive')

            }, interval * 1000)
        }
    }

    _ping(interval) {
        const _this = this

        if (interval > 0) {
            setInterval(async function f() {
                if (_this._connect_f) {
                    _this._ws.send('')
                }
            }, interval * 1000)
        }
    }

    async _get_table(url, config, params) {
        let message = await this.call_rpc(url, params)
        if (params['field_arr']) {
            let message_named = []
            message.forEach((element) => {
                let record = {}
                params['field_arr'].forEach((field_name, i) => {
                    record[field_name] = element[i]
                })
                message_named.push(record)
            })
            message = message_named
        }
        if (params['format_fn']) {
            return params['format_fn'](message)
        }
        return message
    }
}


class Ws {
    constructor(token, wss = false) {
        this._wss = wss
        this.notify = new EventTarget()
        this.online_connections = {}  // {path, ws}
    }


    receive_notify(d) {
        console.log(d)
    }

    call(path, data = {}, notify = false) {
        return new Promise((resolve, reject) => {
            let protocol = 'ws'
            if (this._wss) {
                protocol = 'wss'
            }

            let url = `${protocol}://${location.hostname}:${location.port}/${path}`
            console.log(url)
            let socket = new WebSocket(url)

            socket.onerror = function (e) {
                reject(e)
            }
            socket.onopen = function (e) {
                socket.send(data)
            }
            socket.onmessage = function (d) {
                if (this.receive_notify) {
                    try {
                        let msg = JSON.parse(d.data)
                        this.notify.dispatchEvent(new CustomEvent(msg.method, {detail: msg.params}))
                    } catch (e) {
                        console.log('notify_error', d.data)
                    }
                } else {
                    resolve(d.data)
                }
            }.bind(this)
            socket.onclose = function (d){
                if(notify){
                    FW2.on_close_ws()
                }
            }.bind(this)
        })
    }

}

export {fw2fn, FW2, Ws}
