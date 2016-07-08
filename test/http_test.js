var http = require('http');
//http://www.tuicool.com/articles/iqQFBn
http.createServer(function(request, response){
    response.writeHead(200, {"Content-Type": 'text/plain'});
    response.end('Hello world\n');
}).listen(8888);

console.log('server running at 8888')
