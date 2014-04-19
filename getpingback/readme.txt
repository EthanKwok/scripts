
[简介]

这个脚本是一个辅助Pingback测试的工具，通过adb与设备建立连接，然后监听logcat里面设备发送的pingback请求信息，之后呈献给tester.

[使用情景]

对于当前版本，设计的使用情景如下：
1）用户启动脚本然后输入待测设备的IP地址；
2）用户在待测设备上进行操作；
3）用户查看脚本的输出，进行判断；

[系统要求]

1）可用的adb环境并且adb已被加入环境变量
2）可用的Python2.X环境（release中包含window版本的Python安装包）

[HowTo] 

1. 双击python-2.7.6.msi然后按照提示安装。
2. 双击getPingback_v0.2.py然后按照提示进行测试。

Note: python环境只需要安装一次，以后不用再次安装.

[ChangeList]

1.监听普通频道里面内容的r和pr

[Todo]

1. 监听请求资源的URL然后自动对比更多字段。