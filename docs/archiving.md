### Create Archive


#### Prequisites

Get latest db-dump and audio-files:
   
```shell
mkdir dump && mkdir remote

sshfs -p 61002 aasftp@audioasyl.net:/ ./remote/
rsync -av  ./remote/ ./dump/
```

Load db-dump
   
```mysql
CREATE DATABASE audioasyl CHARACTER SET utf8 COLLATE utf8_general_ci;
```

```shell
mysql -u root -p audioasyl < ./dump/audioasyl.sql
```



#### Install Archiver

```shell
# create a virtualenv - python3.6 required 
virtualenv -p python3 ./venv
source ./venv/bin/activate

pip install -e git+https://github.com/ohrstrom/audioasyl-archiver.git#egg=audioasyl-archiver
```


#### Run Archiver

```shell
# see:
archiver --help
# and
archiver archive --help
```

```shell
# example
archiver -v INFO archive \
-s /storage/audioasyl/dump/audio/ \
-d /storage/audioasyl/archive/ \
-h mysql://root:root@localhost:3306/audioasyl \
playlist
```
