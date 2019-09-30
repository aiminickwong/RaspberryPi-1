# bash complete

## 参考文档

* [Creating a bash completion script](https://iridakos.com/tutorials/2018/03/01/bash-programmable-completion-tutorial.html)
* [跟我一起写shell补全脚本（Bash篇）](https://segmentfault.com/a/1190000002968878)
* [github iridakos/goto](https://github.com/iridakos/goto)

## git补全原理

* bash启动的时候，会加载`/etc/bash_completion.d`中的文件，并执行`. /etc/bash_completion`
* `ls /etc/bash_completion.d`
  ```
  git-prompt
  ```

## 示例

* `cat dothis`
  ```
  #/usr/bin/env bash
  
  _dothis_completions()
  {
    COMPREPLY+=("now")
    COMPREPLY+=("tomorrow")
    COMPREPLY+=("never")
  }
  
  complete -F _dothis_completions dothis
  ```
* `sudo cp dothis /etc/bash_completion.d/`
* `sudo cp dothis /bin`
* `bash`
* `dothis <tab><tab>`
  ```
  never     now       tomorrow
  ```