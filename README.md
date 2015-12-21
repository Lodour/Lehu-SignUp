# 乐乎pt自动签到
学习Python中Requests库时写的脚本，可以挂在服务器上每日自动签到并邮件返回签到结果。

## 用法
* 上传**LehuRegister.py**到服务器目录
* **crontab -e**
* 添加计划任务，如**30 \*/6 * * * python LehuRegister.py**