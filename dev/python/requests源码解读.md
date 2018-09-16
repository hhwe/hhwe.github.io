requests库应该是python最知名的包之一了, 其源码也是python项目规范经典, 最近也在学go, 发现go的net/http和requests库很相识, 看下requests源码加深对http的理解. 

## 简单使用

requests的get, post, delete, patch... 等方法都是通过调用request方法实现的, 
而request()会调用session来处理请求
``` python
def get(url, params=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, **kwargs)

def request(method, url, **kwargs):
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)

# 默认情况下，当你进行网络请求后，响应体会立即被下载。你可以通过 `stream` 参数覆盖这个行为，推迟下载响应体直到访问`Response.content`属性：
r = requests.get(url, stream=True)
# 此时仅有响应头被下载下来了，连接保持打开状态，因此允许我们根据条件获取内容,可以使用Response.iter_content()或iter_lines()来控制工作流, 或者Response.raw直接从urllib3读取响应体
```


requests会自动解码response的内容
``` python
# Response的工作流会有`urllib3`自动解压缩和解码
def iter_content(self, chunk_size=1, decode_unicode=False):
    def generate():
        try:
            for chunk in self.raw.stream(chunk_size, decode_content=True):
                yield chunk
        ...
        if decode_unicode:
            chunks = stream_decode_response_unicode(chunks, self)
        return chunks

def content(self):
    ''' 会从iter_content中分片读取数据
          self._content = b''.join(self.iter_content(CONTENT_CHUNK_SIZE)) or b''
    '''
    return self._content

 def text(self):
    try:  # 根据内容编码解码content
        content = str(self.content, encoding, errors='replace')
    except (LookupError, TypeError):
        content = str(self.content, errors='replace')
    return content


def apparent_encoding(self):
    return chardet.detect(self.content)['encoding']
```

requests中可以自动解析状态并抛出异常
``` python
    def raise_for_status(self):
        """Raises stored :class:`HTTPError`, if one occurred."""
        http_error_msg = ''
        if isinstance(self.reason, bytes):
            try: # 因为有些服务器会做本地化处理, 所以需要对内容先用解码(默认用utf-8
                reason = self.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = self.reason.decode('iso-8859-1')
        else:
            reason = self.reason
        if 400 <= self.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (self.status_code, reason, self.url)
        elif 500 <= self.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (self.status_code, reason, self.url)
        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)
```

## requests的对象
### Session
所有请求方法都会包装成Session.request()方法, 这个会保持当前请求上下文, 并且保持TCP连接. 如果在一个session中设置headers, cookies等都会被该session的请求捕获到, 
``` python
s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)  # '{"cookies": {"sessioncookie": "123456789"}}'
```
