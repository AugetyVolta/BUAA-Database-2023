## 启动方法

### 环境要求

本项目采用yarn作为包管理工具，因此运行项目前请自行安装npm以及yarn

### python依赖安装

python依赖在`requirements.txt`文件中，在项目文件夹终端下执行：

```shell
pip install -r requirements.txt
pip3 install django-cors-headers
```

### 项目启动

如果是windows系统：

- 在项目文件夹下开启一个终端，依次运行`initFrontend.bat`，`run_frontend.bat`，启用前端
- **新开启**一个终端（**上一个终端不要关**），运行`run_backend.bat`，启用后端
- 再次**新开启**一个终端（**之前的终端不要关**），运行`run_photo_server.bat`，启用数据存储端口

如果不是windows系统：

- 在项目文件夹下开启一个终端，依次运行

  ```sh
  cd frontend
  yarn install
  yarn run serve
  ```

- **新开启**一个终端（**上一个终端不要关**），运行

  ```sh
  python manage.py runserver 0.0.0.0:8000
  ```
  
- 再次**新开启**一个终端（**之前的终端不要关**），依次运行

  ```sh
  cd media
  python -m http.server 9000
  ```

### 1级管理员账户

具有系统最高管理权限

  ```
  用户名：uuuuu
  密码：123123
  ```

