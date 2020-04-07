### 工具集合
#### 说明
自己做的或收集的工具合集，项目更新中。。。
#### 技术栈
- 前端：vue全家桶 + nuxt
- 后端：python：Flask
- 数据库：MySQL

## 部署
### 后端
1、准备工作
 - conda虚拟环境
 - 安装依赖包
 ```py
 pip install -r requirements.txt
 ```
 2、 启动
 ```py
 python main.py
 ```

### 前端
1、准备工作
安装装[PM2](http://menvscode.com/detail/5ce21943e8c50a0870f41983)
2、项目clone到服务器
```bash
git clone xxx
```
把本地文件的.nuxt、static,package.json、nuxt.config.js，这四个文件夹放到服务器目录文件下
3、运行
cmd进入改目录下，安装依赖：
```bash
npm install
npm run build
```
运行项目命令(若用pm则可省)
```bash
npm start
```
此时运行的是 http://localhost:3000

4、pm2开启进程守护
```bash
pm2 start npm --name "xxx" -- start
# xxx 是项目名称 在package.json中
```

5、修改项目，重新打包，然后重新部署，则需要重新启动 pm2
```bash
pm2 stop xxx   // 先停止

pm2 restart xxx  // 再重启
```

> 前端致敬 [MikuTools](https://tools.miku.ac/)