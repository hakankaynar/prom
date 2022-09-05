import http.server
import sys
from prometheus_client import start_http_server, Counter, Summary
from urllib.parse import urlparse

VAULT_EP=Summary('vault_ep_usage', 'A vault endpoint usage', ['app_name', 'context_path'])
REQ_COUNT=Counter('vault_usage', 'Vault request counter', ['app_name'])


class HandleRequests(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        REQ_COUNT.labels('my_app').inc()
        vp = self.__get_vault_path()
        VAULT_EP.labels('my_app', vp).time()
        VAULT_EP.labels('my_app', vp).observe(1)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Vault Ep POC App","utf-8"))
        self.wfile.close()

    def __get_vault_path(self):
        try:
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            return query_components["vp"]
        except:
            return '/'


if __name__ == "__main__":
    start_http_server(int(sys.argv[3]))
    server = http.server.HTTPServer((sys.argv[1], int(sys.argv[2])), HandleRequests)
    server.serve_forever()
