const http = require('http');
const { name, version } = require('./package');

let started;

const server = http.createServer(function(req, res) {
    let bodySize = 0;
    req.on('data', function(chunk) {
        bodySize += chunk.byteLength;
    });
    req.on('end', function() {
        const time = new Date().toISOString();
        const json = {
            method: req.method,
            url: req.url,
            bodySize,
            time,
            headers: req.headers,
            env: process.env
        };
        res.setHeader('content-type', 'application/json');
        res.setHeader('server', `${name}/${version}`);
        res.setHeader('server-started', started);
        res.write(JSON.stringify(json, null, '\t'));
        res.end(function() {
            console.log(`${time} ${req.method} ${req.url}`);
        })
    })
});

server.listen(process.env.PORT || 8080, () => {
    started = new Date().toISOString();
});
