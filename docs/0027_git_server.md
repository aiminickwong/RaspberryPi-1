# git server

## 参考文档

* [Setting up Your Raspberry Pi as a Git Server](https://www.sitepoint.com/setting-up-your-raspberry-pi-as-a-git-server/)

## steps

* `sudo adduser git`
* `su git`
* `mkdir helloworld.git`
* `cd helloworld.git`
* `git init --bare`
* `git clone git@192.168.31.189:/home/git/helloworld.git`
  ```
  Cloning into 'helloworld'...
  The authenticity of host '192.168.31.189 (192.168.31.189)' can't be established.
  ECDSA key fingerprint is SHA256:8RCzBU02hBV/GA7E9tJpgvpKRDbauZ1dlfQg9FVmOUs.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added '192.168.31.189' (ECDSA) to the list of known hosts.
  git@192.168.31.189's password:
  warning: You appear to have cloned an empty repository.
  ```