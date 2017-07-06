---
title: 利用Hexo将网站部署到GithubPages
date: 2017-07-06 11:47:41
categories: website
tags: 
    - Hexo 
    - github
---

一直想自己搭建一个个人独立博客，我尝试着使用很多方式自己搭建一个网站，但由于水平有限，一直没有搭建好。最终选择了利用Hexo搭建自己博客，挂在了giuhub上。
这是我建立的一个自己的主页，个人觉得用hexo搭建github博客还是比较简单的，希望能给想要搭建个人博客网站的小伙伴们一个参考。

Ps： 本文是在Windows上搭建的，其他OS搭配环境大致相同，如果感到不适请自行Google。

---
# 1.配置开发环境

## 什么是Hexo？

Hexo是一个快速，简单和强大的博客框架。您在Markdown（或其他语言）中撰写帖子，Hexo会在几秒钟内生成具有美丽主题的静态文件。

## 安装
Hexo只需要几分钟的时间。
安装Hexo很容易。但是，您需要首先安装几个其他的东西：
    1. Git
    2. Node.js
如果您的电脑已经有这些，恭喜！只需安装Hexo与npm：
`$ npm install -g hexo-cli`
如果没有，请到官网安装所有要求：
    [Git官网](https://git-scm.com/)下载并安装Git。
    [Node.js官网](http://nodejs.cn/)下载并安装Node.js。

---

# 2.Hexo网站建立

安装Hexo后，运行以下命令在目标中初始化Hexo <folder>。

    $ hexo init <folder>
    $ cd <folder>
    $ npm安装

一旦初始化，您的项目文件夹将如下所示：

    。
    ├──_config.yml
    ├──package.json
    ├──scaffolds
    ├──source
    | ├──_drafts
    | └──_posts
    └──主题

_config.yml: 站点配置文件,您可以在此配置大多数设置。
package.json: 应用数据。该EJS，Stylus和Markdown默认安装的。如果需要，您可以稍后卸载它们。
/scaffolds/: 脚手架文件夹。当您创建一个新帖子时，Hexo将新文件放在脚手架上。
/source/: 源文件夹。这是您放置网站内容的地方。Hexo忽略隐藏的文件和名称前缀为_（下划线）的文件或文件夹- _posts文件夹除外。可渲染文件（例如Markdown，HTML）将被处理并放入该public文件夹，而其他文件将被简单地复制。
/theme/: 主题文件夹。Hexo通过将网站内容与主题相结合来生成一个静态网站。

我选择的是*hexo-theme-next* 主题，个人比较喜欢里面的Mist布局
具体设置内容请看[theme-next](http://theme-next.iissnan.com/) 
*注*：需将下载好的主题文件夹的[.git]文件夹删掉否则将上传不到github

---

# 3.部署到github

登录账号后，在Github页面的右上方选择New repository进行仓库的创建
![github repository](/images/hexo-github.JPG)

配置部署，在项目根目录的文件中修改_config.yml：

    deploy:
      type: git
      repository: https://github.com/yourname/yourname.github.io.git
      branch: master

## 发表一篇文章

在终端输入：
`$ hexo new "title"`
保存后，我们进行本地发布：
`$ hexo server`
打开浏览器，输入：
`http://localhost:4000/`

## 部署github pages
但是毕竟我们目前发布的只有本机看得到，怎么让其他人看到我们写的博客呢？这时候我们来看看博客的部署。

我们只要在终端执行这样的命令即可：

    $ hexo generate
    $ hexo deploy

这时候我们的博客已经部署到网上了，我们可以在浏览器地址输入栏输入我们的网址即可，如我的博客是：yourname.github.io。

*注*： 由于github在国内各种原因可能，你修改的内容无法立即在github上看到，需要等一段时间。

---

以上大致是我部署这个网站的简单步骤，如有以疑问可以QQ问我