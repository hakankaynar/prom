import http.server
from prometheus_client import start_http_server, Counter, Summary
import logging

REQUEST_COUNT=Counter('app_requests_count', 'Total application http request count', ['app_name', 'context_path'])
REQUEST_LATENCY=Summary('app_request_latency', 'Application request latency')
APP_PORT = 10000
METRICS_PORT = 8001


class HandleRequests(http.server.BaseHTTPRequestHandler):

    @REQUEST_LATENCY.time()
    def do_GET(self):
        logging.info("Handling get request")
        REQUEST_COUNT.labels("my_app", self.path).inc()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            "<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application.</center></h2></body></html>",
            "utf-8"))
        self.wfile.close()


if __name__ == "__main__":
    logging.info("Starting the application")
    start_http_server(METRICS_PORT)
    server = http.server.HTTPServer(('my_app', APP_PORT), HandleRequests)
    server.serve_forever()
