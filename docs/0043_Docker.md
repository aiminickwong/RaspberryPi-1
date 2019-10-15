# Create Raspbian Image

## 参考

* [Docker — 从入门到实践](https://yeasy.gitbooks.io/docker_practice/)
* [Release for Raspberry Pi 4 (Raspbian Buster)](https://forums.docker.com/t/release-for-raspberry-pi-4-raspbian-buster/77120)
* [How to Install Docker on Your Raspberry Pi](https://howchoo.com/g/nmrlzmq1ymn/how-to-install-docker-on-your-raspberry-pi)
* [树莓派卡片电脑安装 Docker CE](https://yeasy.gitbooks.io/docker_practice/install/raspberry-pi.html)

## Install Docker

* `sudo curl -sL get.docker.com | sed 's/9)/10)/' | sh`
  ```
  # Executing docker install script, commit: f45d7c11389849ff46a6b4d94e0dd1ffebca32c1
  + sh -c apt-get update -qq >/dev/null
  + sh -c DEBIAN_FRONTEND=noninteractive apt-get install -y -qq apt-transport-https ca-certificates curl >/dev/null
  + sh -c curl -fsSL "https://download.docker.com/linux/raspbian/gpg" | apt-key add -qq - >/dev/null
  Warning: apt-key output should not be parsed (stdout is not a terminal)
  + sh -c echo "deb [arch=armhf] https://download.docker.com/linux/raspbian buster stable" > /etc/apt/sources.list.d/docker.list
  + sh -c apt-get update -qq >/dev/null
  + [ -n  ]
  + sh -c apt-get install -y -qq --no-install-recommends docker-ce >/dev/null
  + sh -c docker version
  Client: Docker Engine - Community
   Version:           19.03.3
   API version:       1.40
   Go version:        go1.12.10
   Git commit:        a872fc2
   Built:             Tue Oct  8 01:12:14 2019
   OS/Arch:           linux/arm
   Experimental:      false
  
  Server: Docker Engine - Community
   Engine:
    Version:          19.03.3
    API version:      1.40 (minimum version 1.12)
    Go version:       go1.12.10
    Git commit:       a872fc2
    Built:            Tue Oct  8 01:06:12 2019
    OS/Arch:          linux/arm
    Experimental:     false
   containerd:
    Version:          1.2.6
    GitCommit:        894b81a4b802e4eb2a91d1ce216b8817763c29fb
   runc:
    Version:          1.0.0-rc8
    GitCommit:        425e105d5a03fabd737a126ad93d62a9eeede87f
   docker-init:
    Version:          0.18.0
    GitCommit:        fec3683
  If you would like to use Docker as a non-root user, you should now consider
  adding your user to the "docker" group with something like:
  
    sudo usermod -aG docker your-user
  
  Remember that you will have to log out and back in for this to take effect!
  
  WARNING: Adding a user to the "docker" group will grant the ability to run
           containers which can be used to obtain root privileges on the
           docker host.
           Refer to https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface
           for more information.
  ```
* `ps aux | grep docker`
  ```
  root     16095  0.3  1.5 966720 59340 ?        Ssl  11:48   0:00 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
  root     18548  0.0  0.0   7348   544 pts/0    S+   11:52   0:00 grep docker
  ```
* `sudo docker run arm32v7/hello-world`
  ```
  Unable to find image 'arm32v7/hello-world:latest' locally
  latest: Pulling from arm32v7/hello-world
  c1eda109e4da: Pull complete
  Digest: sha256:07e995a680212a0a8a01e181b3fff128d44b8fe0c11426b638ec3cde7273f0a3
  Status: Downloaded newer image for arm32v7/hello-world:latest
  
  Hello from Docker!
  This message shows that your installation appears to be working correctly.
  
  To generate this message, Docker took the following steps:
   1. The Docker client contacted the Docker daemon.
   2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
      (arm32v7)
   3. The Docker daemon created a new container from that image which runs the
      executable that produces the output you are currently reading.
   4. The Docker daemon streamed that output to the Docker client, which sent it
      to your terminal.
  
  To try something more ambitious, you can run an Ubuntu container with:
   $ docker run -it ubuntu bash
  
  Share images, automate workflows, and more with a free Docker ID:
   https://hub.docker.com/
  
  For more examples and ideas, visit:
   https://docs.docker.com/get-started/
  ```

## docker usage

* 镜像列表：`sudo docker image ls`
  ```
  REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
  pi-gen                latest              4e6c4d51957e        14 hours ago        469MB
  debian                buster              1cbe61c6db74        4 weeks ago         92.8MB
  arm32v7/hello-world   latest              618e43431df9        9 months ago        1.64kB
  ```
* 启动docker image:
  * `sudo docker run -it debian bash`
  * `sudo docker run -it --rm debian bash`: Docker containers are not automatically removed when you stop them unless you start the container using the `--rm` flag.
* 查看docker进程：
  * `sudo docker container ls -a`
  * `sudo docker ps -n 3`
    ```
    CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS                      PORTS               NAMES
    bedef41a0231        arm32v7/hello-world   "/hello"                 53 minutes ago      Exited (0) 52 minutes ago                       sad_engelbart
    f811f0c69ddd        pi-gen                "bash -e -o pipefail…"   14 hours ago        Exited (1) 14 hours ago                         pigen_work
    ```
* 停止docker进程：`sudo docker stop bedef41a0231`
  ```
  bedef41a0231
  ```
* 删除Container ID：`sudo docker rm bedef41a0231`
  ```
  bedef41a0231
  ```
* 删除image（删除前需要停止进程）：
  * `sudo docker image rm debian`
    ```
    Untagged: debian:latest
    ```
  * `sudo docker image rm 618e43431df9 -f`
    ```
    Untagged: arm32v7/hello-world:latest
    Untagged: arm32v7/hello-world@sha256:07e995a680212a0a8a01e181b3fff128d44b8fe0c11426b638ec3cde7273f0a3
    Deleted: sha256:618e43431df9635eee9cf7224aa92c8d6f74aa36cd3b2359604389ca36e79380
    ```
* 启动使用一个docker image：
  * 创建container：`sudo docker run -it debian bash`
  * 在中断中CTRL+p、CTRL+q来detach；
  * 查看docker container id：`sudo docker ps -a`
  * 重新进入container：`sudo docker attach <container id>
  * 后台启动container：`sudo docker start <container id>

## Docker挂载目录

* [Docker 数据管理](https://yeasy.gitbooks.io/docker_practice/data_management/)