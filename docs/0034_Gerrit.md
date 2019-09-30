# Gerrit

## 简介

Gerrit是Google为Android系统研发量身定制的一套免费开源的代码审核系统，它在传统的源码管理协作流程中强制性引入代码审核机制，通过人工代码审核和自动化代码验证过程，将不符合要求的代码屏蔽在代码库之外，确保核心代码多人校验、多人互备和自动化构建核验。

## git/OpenJDK Version

* `java --version`
  ```
  openjdk 11.0.3 2019-04-16
  OpenJDK Runtime Environment (build 11.0.3+7-post-Raspbian-5)
  OpenJDK Server VM (build 11.0.3+7-post-Raspbian-5, mixed mode)
  ```
* `git --version`
  ```
  git version 2.20.1
  ```

## 添加用户

* `sudo adduser gerrit`
* `sudo usermod -a -G sudo gerrit`
* `sudo su gerrit`

## gerrit download

* https://gerrit-releases.storage.googleapis.com/index.html
* `sudo su gerrit`
* `wget https://gerrit-releases.storage.googleapis.com/gerrit-2.16.7.war`
* `java -jar gerrit-2.16.7.war init -d review_site`
  ```
  gerrit@raspberrypi:~ $ java -jar gerrit-2.16.7.war init -d review_site
  WARNING: An illegal reflective access operation has occurred
  WARNING: Illegal reflective access by com.google.inject.internal.cglib.core.$ReflectUtils$1 (file:/hong.ClassLoader.defineClass(java.lang.String,byte[],int,int,java.security.ProtectionDomain)
  WARNING: Please consider reporting this to the maintainers of com.google.inject.internal.cglib.core.$
  WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
  WARNING: All illegal access operations will be denied in a future release
  Using secure store: com.google.gerrit.server.securestore.DefaultSecureStore
  [2019-09-27 02:48:37,626] [main] INFO  com.google.gerrit.server.config.GerritServerConfigProvider : N
  
  *** Gerrit Code Review 2.16.7
  ***
  
  Create '/home/gerrit/review_site' [Y/n]? y
  
  *** Git Repositories
  ***
  
  Location of Git repositories   [git]:
  
  *** SQL Database
  ***
  
  Database server type           [h2]:
  
  *** NoteDb Database
  ***
  
  Use NoteDb for change metadata?
    See documentation:
    https://gerrit-review.googlesource.com/Documentation/note-db.html
  Enable                         [Y/n]? y
  
  *** Index
  ***
  
  Type                           [lucene/?]:
  
  *** User Authentication
  ***
  
  Authentication method          [openid/?]: http
  Get username from custom HTTP header [y/N]?
  SSO logout URL                 :
  Enable signed push support     [y/N]?
  
  *** Review Labels
  ***
  
  Install Verified label         [y/N]?
  
  *** Email Delivery
  ***
  
  SMTP server hostname           [localhost]:
  SMTP server port               [(default)]:
  SMTP encryption                [none/?]:
  SMTP username                  :
  
  *** Container Process
  ***
  
  Run as                         [gerrit]:
  Java runtime                   [/usr/lib/jvm/java-11-openjdk-armhf]:
  Copy gerrit-2.16.7.war to review_site/bin/gerrit.war [Y/n]?
  Copying gerrit-2.16.7.war to review_site/bin/gerrit.war
  
  *** SSH Daemon
  ***
  
  Listen on address              [*]:
  Listen on port                 [29418]:
  Generating SSH host key ... rsa... ed25519... ecdsa 256... ecdsa 384... ecdsa 521... done
  
  *** HTTP Daemon
  ***
  
  Behind reverse proxy           [y/N]?
  Use SSL (https://)             [y/N]?
  Listen on address              [*]:
  Listen on port                 [8080]:
  Canonical URL                  [http://raspberrypi:8080/]:
  
  *** Cache
  ***
  
  
  *** Plugins
  ***
  
  Installing plugins.
  Install plugin codemirror-editor version v2.16.7 [y/N]?
  Install plugin commit-message-length-validator version v2.16.7 [y/N]?
  Install plugin download-commands version v2.16.7 [y/N]?
  Install plugin hooks version v2.16.7 [y/N]?
  Install plugin replication version v2.16.7 [y/N]?
  Install plugin reviewnotes version v2.16.7 [y/N]?
  Install plugin singleusergroup version v2.16.7 [y/N]?
  Initializing plugins.
  No plugins found with init steps.
  
  Initialized /home/gerrit/review_site
  Reindexing projects:    100% (2/2) with: reindex --site-path review_site --threads 1 --index projects
  Reindexed 2 documents in projects index in 1.1s (1.9/s)
  Executing /home/gerrit/review_site/bin/gerrit.sh start
  Starting Gerrit Code Review: WARNING: Could not adjust Gerrit's process for the kernel's out-of-memor
           This may be caused by /home/gerrit/review_site/bin/gerrit.sh not being run as root.
           Consider changing the OOM score adjustment manually for Gerrit's PID= with e.g.:
           echo '-1000' | sudo tee /proc//oom_score_adj
  FAILED
  error: cannot start Gerrit: exit status 1
  Waiting for server on raspberrypi:8080 ...
  ```
* 修改`review_site/etc/gerrit.config`中的ip地址
  ```
  [gerrit]
          basePath = git
          serverId = 7c6e48d3-270e-445c-9a51-5be6b92417be
          canonicalWebUrl = http://192.168.20.96:8080/
  [database]
          type = h2
          database = /home/gerrit/review_site/db/ReviewDB
  [noteDb "changes"]
          disableReviewDb = true
          primaryStorage = note db
          read = true
          sequence = true
          write = true
  [container]
          javaOptions = "-Dflogger.backend_factory=com.google.common.flogger.backend.log4j.Log4jBackendFactory#getInstance"
          javaOptions = "-Dflogger.logging_context=com.google.gerrit.server.logging.LoggingContext#getInstance"
          user = gerrit
          javaHome = /usr/lib/jvm/java-11-openjdk-armhf
  [index]
          type = LUCENE
  [auth]
          type = HTTP
  [receive]
          enableSignedPush = false
  [sendemail]
          smtpServer = localhost
  [sshd]
          listenAddress = *:29418
  [httpd]
          listenUrl = http://*:8080/
  [cache]
          directory = cache
  ```
* `java -jar gerrit-2.16.7.war init -d review_site`
  ```
  gerrit@raspberrypi:~ $ java -jar gerrit-2.16.7.war init -d review_site
  WARNING: An illegal reflective access operation has occurred
  WARNING: Illegal reflective access by com.google.inject.internal.cglib.core.$ReflectUtils$1 (file:/home/gerrit/.gerritcodereview/tmp/gerrit_17917946062353911876_app/guice-4.2.1.jar) to method java.lang.ClassLoader.defineClass(java.lang.String,byte[],int,int,java.security.ProtectionDomain)
  WARNING: Please consider reporting this to the maintainers of com.google.inject.internal.cglib.core.$ReflectUtils$1
  WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
  WARNING: All illegal access operations will be denied in a future release
  Using secure store: com.google.gerrit.server.securestore.DefaultSecureStore
  
  *** Gerrit Code Review 2.16.7
  ***
  
  
  *** Git Repositories
  ***
  
  Location of Git repositories   [git]:
  
  *** SQL Database
  ***
  
  Database server type           [h2]:
  
  *** Index
  ***
  
  Type                           [lucene/?]:
  
  The index must be rebuilt before starting Gerrit:
    java -jar gerrit.war reindex -d site_path
  
  *** User Authentication
  ***
  
  Authentication method          [http/?]:
  Get username from custom HTTP header [y/N]?
  SSO logout URL                 :
  Enable signed push support     [y/N]?
  
  *** Review Labels
  ***
  
  Install Verified label         [y/N]?
  
  *** Email Delivery
  ***
  
  SMTP server hostname           [localhost]:
  SMTP server port               [(default)]:
  SMTP encryption                [none/?]:
  SMTP username                  :
  
  *** Container Process
  ***
  
  Run as                         [gerrit]:
  Java runtime                   [/usr/lib/jvm/java-11-openjdk-armhf]:
  Upgrade review_site/bin/gerrit.war [Y/n]?
  Copying gerrit-2.16.7.war to review_site/bin/gerrit.war
  
  *** SSH Daemon
  ***
  
  Listen on address              [*]:
  Listen on port                 [29418]:
  
  *** HTTP Daemon
  ***
  
  Behind reverse proxy           [y/N]?
  Use SSL (https://)             [y/N]?
  Listen on address              [*]:
  Listen on port                 [8080]:
  Canonical URL                  [http://192.168.20.96:8080/]:
  
  *** Cache
  ***
  
  Delete cache file /home/gerrit/review_site/cache/diff_summary.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/change_kind.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/diff.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/conflicts.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/mergeability.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/diff_intraline.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/oauth_tokens.h2.db [y/N]?
  Delete cache file /home/gerrit/review_site/cache/git_tags.h2.db [y/N]?
  
  *** Plugins
  ***
  
  Installing plugins.
  Install plugin codemirror-editor version v2.16.7 [y/N]?
  Install plugin commit-message-length-validator version v2.16.7 [y/N]?
  Install plugin download-commands version v2.16.7 [y/N]?
  Install plugin hooks version v2.16.7 [y/N]?
  Install plugin replication version v2.16.7 [y/N]?
  Install plugin reviewnotes version v2.16.7 [y/N]?
  Install plugin singleusergroup version v2.16.7 [y/N]?
  Initializing plugins.
  No plugins found with init steps.
  
  Initialized /home/gerrit/review_site
  Reindexing projects:    100% (2/2) with: reindex --site-path review_site --threads 1 --index projects
  Reindexed 2 documents in projects index in 0.6s (3.4/s)
  ```
* `/home/gerrit/review_site/bin/gerrit.sh`
  ```
  [...省略]
  # START_STOP_DAEMON
  #   If set to "0" disables using start-stop-daemon.  This may need to
  #   be set on SuSE systems.
  
  # $site_path
  GERRIT_SITE=/home/gerrit/review_site

  [...省略]
  ```
* `review_site/bin/gerrit.sh restart`
* `sudo cp review_site/bin/gerrit.sh /etc/init.d/gerrit`
* `sudo update-rc.d gerrit defaults 21`
* `sudo service gerrit restart`
* `sudo systemctl status gerrit.service`
* `cat ~/review_site/logs/error_log`
  ```
  [2019-09-28 06:04:55,037] [main] INFO  com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SshCommandStart' queue
  [2019-09-28 06:04:57,942] [main] WARN  com.google.gerrit.sshd.SshDaemon : Cannot format SSHD host key [EdDSA]: invalid key type
  [2019-09-28 06:04:57,946] [main] INFO  com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SSH-Stream-Worker' queue
  [2019-09-28 06:04:57,958] [main] INFO  com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SSH-Interactive-Worker' queue
  [2019-09-28 06:04:57,961] [main] INFO  com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SSH-Batch-Worker' queue
  [2019-09-28 06:04:58,088] [main] WARN  com.google.gerrit.server.config.GitwebCgiConfig : gitweb not installed (no /usr/lib/cgi-bin/gitweb.cgi found)
  [2019-09-28 06:05:01,355] [main] INFO  org.eclipse.jetty.util.log : Logging initialized @67534ms to org.eclipse.jetty.util.log.Slf4jLog
  [2019-09-28 06:05:01,829] [main] ERROR com.google.gerrit.pgm.Daemon : Unable to start daemon
  java.lang.reflect.InaccessibleObjectException: Unable to make public long com.sun.management.internal.OperatingSystemImpl.getProcessCpuTime() accessible: module jdk.management does not "opens com.sun.management.internal" to unnamed module @32d386
          at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:340)
          at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:280)
          at java.base/java.lang.reflect.Method.checkCanSetAccessible(Method.java:198)
          at java.base/java.lang.reflect.Method.setAccessible(Method.java:192)
          at com.google.gerrit.metrics.proc.OperatingSystemMXBeanProvider.<init>(OperatingSystemMXBeanProvider.java:55)
          at com.google.gerrit.metrics.proc.OperatingSystemMXBeanProvider.<init>(OperatingSystemMXBeanProvider.java:23)
          at com.google.gerrit.metrics.proc.OperatingSystemMXBeanProvider$Factory.create(OperatingSystemMXBeanProvider.java:40)
          at com.google.gerrit.metrics.proc.ProcMetricModule.procCpuUsage(ProcMetricModule.java:65)
          at com.google.gerrit.metrics.proc.ProcMetricModule.configure(ProcMetricModule.java:38)
          at com.google.gerrit.metrics.proc.MetricModule$1.start(MetricModule.java:36)
          at com.google.gerrit.lifecycle.LifecycleManager.start(LifecycleManager.java:95)
          at com.google.gerrit.pgm.Daemon.start(Daemon.java:345)
          at com.google.gerrit.pgm.Daemon.run(Daemon.java:251)
          at com.google.gerrit.pgm.util.AbstractProgram.main(AbstractProgram.java:61)
          at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
          at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
          at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
          at java.base/java.lang.reflect.Method.invoke(Method.java:566)
          at com.google.gerrit.launcher.GerritLauncher.invokeProgram(GerritLauncher.java:224)
          at com.google.gerrit.launcher.GerritLauncher.mainImpl(GerritLauncher.java:120)
          at com.google.gerrit.launcher.GerritLauncher.main(GerritLauncher.java:65)
          at Main.main(Main.java:28)
  ```
* `sudo apt-get install gitweb`
* `cat ~/review_site/logs/error_log`
  ```
  [2019-09-28 07:28:07,239] [main] INFO com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SshCommandStart' queue
  [2019-09-28 07:28:09,333] [main] WARN com.google.gerrit.sshd.SshDaemon : Cannot format SSHD host key [EdDSA]: invalid key type
  [2019-09-28 07:28:09,335] [main] INFO com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SSH-Stream-Worker' queue
  [2019-09-28 07:28:09,341] [main] INFO com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SSH-Interactive-Worker' queue
  [2019-09-28 07:28:09,343] [main] INFO com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SSH-Batch-Worker' queue
  [2019-09-28 07:28:13,540] [main] INFO org.eclipse.jetty.util.log : Logging initialized @123670ms to org.eclipse.jetty.util.log.Slf4jLog
  [2019-09-28 07:28:13,966] [main] ERROR com.google.gerrit.pgm.Daemon : Unable to start daemon
  java.lang.reflect.InaccessibleObjectException: Unable to make public long com.sun.management.internal.OperatingSystemImpl.getProcessCpuTime() accessible: module jdk.management does not "opens com.sun.management.internal" to unnamed module @32d386
  at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:340)
  at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:280)
  at java.base/java.lang.reflect.Method.checkCanSetAccessible(Method.java:198)
  at java.base/java.lang.reflect.Method.setAccessible(Method.java:192)
  at com.google.gerrit.metrics.proc.OperatingSystemMXBeanProvider.(OperatingSystemMXBeanProvider.java:55)
  at com.google.gerrit.metrics.proc.OperatingSystemMXBeanProvider.(OperatingSystemMXBeanProvider.java:23)
  at com.google.gerrit.metrics.proc.OperatingSystemMXBeanProvider$Factory.create(OperatingSystemMXBeanProvider.java:40)
  at com.google.gerrit.metrics.proc.ProcMetricModule.procCpuUsage(ProcMetricModule.java:65)
  at com.google.gerrit.metrics.proc.ProcMetricModule.configure(ProcMetricModule.java:38)
  at com.google.gerrit.metrics.proc.MetricModule$1.start(MetricModule.java:36)
  at com.google.gerrit.lifecycle.LifecycleManager.start(LifecycleManager.java:95)
  at com.google.gerrit.pgm.Daemon.start(Daemon.java:345)
  at com.google.gerrit.pgm.Daemon.run(Daemon.java:251)
  at com.google.gerrit.pgm.util.AbstractProgram.main(AbstractProgram.java:61)
  at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
  at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
  at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
  at java.base/java.lang.reflect.Method.invoke(Method.java:566)
  at com.google.gerrit.launcher.GerritLauncher.invokeProgram(GerritLauncher.java:224)
  at com.google.gerrit.launcher.GerritLauncher.mainImpl(GerritLauncher.java:120)
  at com.google.gerrit.launcher.GerritLauncher.main(GerritLauncher.java:65)
  at Main.main(Main.java:28)
  [2019-09-28 07:28:23,027] [main] INFO com.google.gerrit.server.git.WorkQueue : Adding metrics for 'SshCommandStart' queue
  ```
* 错误解释
  * [Issue 7347: Error launching gerrit with Java 1.9](https://bugs.chromium.org/p/gerrit/issues/detail?id=7347)
  * [Issue 7843: Gerrit 2.14.5.1 fails to start with Java version above 8](https://bugs.chromium.org/p/gerrit/issues/detail?id=7843)


## 结论

如上报错可知，目前gerrit貌似暂时无法在树莓派Buster版本上运行；