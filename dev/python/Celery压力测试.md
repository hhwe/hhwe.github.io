# owlscrapy测试问题

测试总共3台机器:
10.0.5.152: 双线程 4GB
10.0.5.169: 单线程 1GB
10.0.5.170: 单线程 1GB

## 单点测试

10.0.5.170, worker: 2个
worker | 任务数 | 开始时间 | 结束时间 | 总时间
--- | --- | --- | --- | ---
2 | 200 | 13:35 | 14:23 | 48
2 | 200 | 14:24 |  15:17 | 53

![2个worker消费200个任务结果1](https://upload-images.jianshu.io/upload_images/13148580-0f54fd5f4d9da2bf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![2个worker消费200个任务结果2](https://upload-images.jianshu.io/upload_images/13148580-71de901e65c5af42.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

10.0.5.169, worker: 3个; 10.0.5.170, worker: 3个
worker | 任务数 | 开始时间 | 结束时间 | 总时间
--- | --- | --- | --- | ---
6 | 100 | 15:42 | 16:01 | 19
6 | 100 | 11:24 | 11:33 | 9

![6个worker消费100个任务结果1](https://upload-images.jianshu.io/upload_images/13148580-2ec74f94615c438d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![6个worker消费100个任务结果2](https://upload-images.jianshu.io/upload_images/13148580-bdae2785c029a15a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 测试结论

**问题**: 会出现chrome一直占用内存, 没有关闭
![chrome会常驻内存](https://upload-images.jianshu.io/upload_images/13148580-02c83fcfb40e53a6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**可能出现**: 
a. 在node中启动chrome但是时间过长, celery将node杀死, 
b.任务还在做 的时候重启celery
**解决方式**: 在python中获取node的pid, 在任务失败的时候, 关闭所有ppid的pid的进程
**待解决**: 无法得知chrome是否的ppid是否是node的pid

查看进程依赖
1. 单个worker
```
# celery进程
ubuntu   17496 17492  0 13:58 ?        00:00:02 /home/ubuntu/owlscrapy/venv/bin/python /home/ubuntu/owlscrapy/venv/bin/celery worker -A tasks.scrapyTask -Q snapshot -c 1 -P gevent -l info --hostname 169@snapshot

# node进程
ubuntu   17825 17496 12 14:08 ?        00:00:00 /usr/bin/node /home/ubuntu/owlscrapy/scrapy/scrapy.js -c {} -u http://www.taobao.com

# chrome进程
ubuntu   17835 17825 15 14:08 ?        00:00:03 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --disable-background-networking --disable-background-timer-throttling --disable-breakpad --disable-client-side-phishing-detection --disable-default-apps --disable-dev-shm-usage --disable-extensions --disable-features=site-per-process --disable-hang-monitor --disable-popup-blocking --disable-prompt-on-repost --disable-sync --disable-translate --metrics-recording-only --no-first-run --safebrowsing-disable-auto-update --enable-automation --password-store=basic --use-mock-keychain --remote-debugging-port=0 --user-data-dir=/tmp/puppeteer_dev_profile-vLT9Vn --headless --disable-gpu --hide-scrollbars --mute-audio
ubuntu   17838 17835  0 14:08 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   17840 17838  0 14:08 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   17856 17840  0 14:08 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=8165675338679765598 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=8165675338679765598 --renderer-client-id=2 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   17857 17835  0 14:08 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=gpu-process --disable-features=site-per-process --disable-breakpad --headless --headless --gpu-preferences=KAAAAAAAAACAAABAAQAAAAAAAAAAAGAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --use-gl=swiftshader-webgl --override-use-software-gl-for-tests --headless --service-request-channel-token=10760726567322150560
ubuntu   17867 17840 26 14:08 ?        00:00:05 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=235682233902937114 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=235682233902937114 --renderer-client-id=4 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   17878 17857  0 14:08 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=-broker
```
2. 两个worker
```
# celery 进程
ubuntu   18678 17968 14 14:40 ?        00:00:01 /home/ubuntu/owlscrapy/venv/bin/python /home/ubuntu/owlscrapy/venv/bin/celery worker -A tasks.scrapyTask -Q snapshot -c 2 -P gevent -l info --hostname 169@snapshot

# node 
ubuntu   18817 18678  1 14:43 ?        00:00:00 /usr/bin/node /home/ubuntu/owlscrapy/scrapy/scrapy.js -c {} -u http://www.baidu.com
ubuntu   18874 18678  1 14:43 ?        00:00:00 /usr/bin/node /home/ubuntu/owlscrapy/scrapy/scrapy.js -c {} -u http://www.baidu.com

# chrome进程
ubuntu   18827 18817  1 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --disable-background-networking --disable-background-timer-throttling --disable-breakpad --disable-client-side-phishing-detection --disable-default-apps --disable-dev-shm-usage --disable-extensions --disable-features=site-per-process --disable-hang-monitor --disable-popup-blocking --disable-prompt-on-repost --disable-sync --disable-translate --metrics-recording-only --no-first-run --safebrowsing-disable-auto-update --enable-automation --password-store=basic --use-mock-keychain --remote-debugging-port=0 --user-data-dir=/tmp/puppeteer_dev_profile-4CDUWH --headless --disable-gpu --hide-scrollbars --mute-audio
ubuntu   18830 18827  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   18832 18830  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   18848 18832  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=12904881541039520949 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=12904881541039520949 --renderer-client-id=2 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   18849 18827  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=gpu-process --disable-features=site-per-process --disable-breakpad --headless --headless --gpu-preferences=KAAAAAAAAACAAABAAQAAAAAAAAAAAGAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --use-gl=swiftshader-webgl --override-use-software-gl-for-tests --headless --service-request-channel-token=17609677285705530563
ubuntu   18859 18832  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=4283502768896892804 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=4283502768896892804 --renderer-client-id=4 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   18869 18849  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=-broker
ubuntu   18884 18874  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --disable-background-networking --disable-background-timer-throttling --disable-breakpad --disable-client-side-phishing-detection --disable-default-apps --disable-dev-shm-usage --disable-extensions --disable-features=site-per-process --disable-hang-monitor --disable-popup-blocking --disable-prompt-on-repost --disable-sync --disable-translate --metrics-recording-only --no-first-run --safebrowsing-disable-auto-update --enable-automation --password-store=basic --use-mock-keychain --remote-debugging-port=0 --user-data-dir=/tmp/puppeteer_dev_profile-OZ48qA --headless --disable-gpu --hide-scrollbars --mute-audio
ubuntu   18887 18884  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   18889 18887  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   18905 18889  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=11863170506900106348 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=11863170506900106348 --renderer-client-id=2 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   18906 18884  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=gpu-process --disable-features=site-per-process --disable-breakpad --headless --headless --gpu-preferences=KAAAAAAAAACAAABAAQAAAAAAAAAAAGAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --use-gl=swiftshader-webgl --override-use-software-gl-for-tests --headless --service-request-channel-token=16813104885650953142
ubuntu   18916 18889  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=6782061170690580289 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=6782061170690580289 --renderer-client-id=4 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   18927 18906  0 14:43 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=-broker

## 如果中途杀掉node的话chrome会一直挂起
ubuntu   19094     1  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --disable-background-networking --disable-background-timer-throttling --disable-breakpad --disable-client-side-phishing-detection --disable-default-apps --disable-dev-shm-usage --disable-extensions --disable-features=site-per-process --disable-hang-monitor --disable-popup-blocking --disable-prompt-on-repost --disable-sync --disable-translate --metrics-recording-only --no-first-run --safebrowsing-disable-auto-update --enable-automation --password-store=basic --use-mock-keychain --remote-debugging-port=0 --user-data-dir=/tmp/puppeteer_dev_profile-Ggea9b --headless --disable-gpu --hide-scrollbars --mute-audio
ubuntu   19097 19094  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   19099 19097  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=zygote --headless --headless
ubuntu   19115 19099  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=2286869522143292856 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=2286869522143292856 --renderer-client-id=2 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   19116 19094  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=gpu-process --disable-features=site-per-process --disable-breakpad --headless --headless --gpu-preferences=KAAAAAAAAACAAABAAQAAAAAAAAAAAGAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --use-gl=swiftshader-webgl --override-use-software-gl-for-tests --headless --service-request-channel-token=6122937731507223986
ubuntu   19126 19099  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=renderer --disable-background-timer-throttling --disable-breakpad --enable-automation --file-url-path-alias=/gen=/home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/gen --use-gl=swiftshader-webgl --disable-features=site-per-process --disable-gpu-compositing --service-pipe-token=4476390582067925563 --lang=en-US --headless --num-raster-threads=1 --service-request-channel-token=4476390582067925563 --renderer-client-id=4 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101
ubuntu   19137 19116  0 14:46 ?        00:00:00 /home/ubuntu/owlscrapy/scrapy/node_modules/_puppeteer@1.6.1@puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --type=-broker
```
可以看出node启动的chrome都是有进程依赖关系的, 当杀死node的时候讲其所有子孙线程全部杀死, 具体实现使用shell脚本形式
```
# !/bin/bash

echo $1
pid=$1

for child in $(ps -o pid,ppid -ax | \
   awk "{ if ( \$2 == $pid ) { print \$1 }}")
do
  echo "Killing child process $child because ppid = $pid"
  kill -9 $child
done

kill -9 $pid
```

### 修改后测试
10.0.5.169, worker: 3个; 10.0.5.170, worker: 3个
worker | 任务数 | 开始时间 | 结束时间 | 总时间/m | 单个任务耗时/s
--- | --- | --- | --- | --- | ---
6 | 780 | 14:31 | 15:58 | 87 | 40.15
6 | 780 | 16:07 | 17:39 | 92 | 42.46

![6个worker消费100个任务结果1](https://upload-images.jianshu.io/upload_images/13148580-6b1da843d11134ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![结束后所有进程情况1](https://upload-images.jianshu.io/upload_images/13148580-4f4c123b293eab3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![6个worker消费100个任务结果2](https://upload-images.jianshu.io/upload_images/13148580-74319f459b8d2190.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![结束后所有进程情况2](https://upload-images.jianshu.io/upload_images/13148580-c6b8ce6de0cf087a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


可以看到所有的任务结束后没有残留的chrome进程, 这两组运行完基本没有特别大的问题, 




