const http = require("http")  

http.createServer(function (request, result) {
    result.writeHead(200, {'Content-Type': 'text/html'});
    if (request.url === "/") {
        result.write(`<h2>This is Danny Liu's homepage!</h2>`)
    } else if (request.url === "/about") {
        result.write(`<h2>This is Danny Liu's about page!</h2>`)
    } else {
        result.write(`<h2>Sorry, your page is not found!!!</h2>
        <a href="/">back to home page</a>`)
    }
    result.end()
}).listen(5000)


