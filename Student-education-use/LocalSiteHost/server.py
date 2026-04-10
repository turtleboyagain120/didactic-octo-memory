import http.server
import socketserver
import urllib.request
import urllib.parse
from urllib.parse import parse_qs
import ssl
PORT = 8000

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path.startswith('/proxy?url='):
      qs = parse_qs(urllib.parse.urlparse(self.path).query)
      target_url = qs.get('url', [''])[0]
      self.send_response(200)
      self.send_header('Content-Type', 'text/html; charset=utf-8')
      self.end_headers()
      html = f'''
<!DOCTYPE html>
<html>
<head><title>Local Site Host</title></head>
<body>
<h1>Local Site Host 🏠🌐</h1>
<form>
<input type="url" name="url" placeholder="https://coolmathgames.com" style="width:500px" value="{target_url}">
<button>Enter!</button>
</form>
<iframe src="/proxy2?url={urllib.parse.quote(target_url)}" width="100%" height="600px"></iframe>
<script>document.querySelector('form').onsubmit = e => {{ e.preventDefault(); location.reload(); }};
</script>
</body>
</html>'''
      self.wfile.write(html.encode())
      return
    elif self.path.startswith('/proxy2?url='):
      qs = parse_qs(urllib.parse.urlparse(self.path).query)
      target_url = qs.get('url', [''])[0]
      targets = [
        "https://webcache.googleusercontent.com/search?q=cache:" + urllib.parse.quote(target_url),
        target_url
      ]
      for url in targets:
        try:
          ctx = ssl.create_default_context()
          ctx.check_hostname = False
          ctx.verify_mode = ssl.CERT_NONE
          req = urllib.request.Request(url)
          req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
          with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            content = response.read(10*1024*1024)
            self.send_response(response.code)
            [self.send_header(key, value) for key, value in response.headers.items() if key.lower() not in ('content-encoding', 'content-length', 'transfer-encoding')]
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
            return
        except Exception as e:
          print(f'Failed {url}: {e}')
          continue
      self.send_response(500)
      self.end_headers()
      self.wfile.write(b'Failed to load site.')
    else:
      super().do_GET()


if __name__ == '__main__':
  with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f'School Proxy on http://localhost:{PORT}/proxy?url=<site>')
    print('Ethical use only!')
    httpd.serve_forever()
