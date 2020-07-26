const http = require('http');

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
        res.write(JSON.stringify(json, null, '\t'));
        res.end(function() {
            console.log(`${time} ${req.method} ${req.url}`);
        })
    })
});

server.listen(process.env.PORT || 8080);
