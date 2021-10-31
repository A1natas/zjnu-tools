# openwrt-shanxunhelper-python

基于python，openwrt-uci模块的路由器移动闪讯电信换网小助手



## 使用方法

下载shanxunhelper.py

**修改相应配置**

然后执行

```shell
python shanxunhelper.py
```

## 编译为exe

git clone本仓库，并安装vituralenv，powershell进入仓库目录输入

```shell
cd .\Script\
.\activate
cd ..
pyinstaller -F --onefile -i icon.ico rebootrouter.py 
```

即可在dist内找到编译完成的exe

## 依赖安装

需要路由器安装luci-mod-uci



## 效果图

非常简陋，希望有大佬改改

![](https://cdn.jsdelivr.net/gh/Xunflash/openwrt-shanxunhelper-python@1.0/photos/xiaoguo.png)

