### Create Archive


#### Prequisites

Get latest db-dump and audio-files:
   
```shell
mkdir dump && mkdir remote

sshfs -p 61002 aasftp@audioasyl.net:/ ./remote/
rsync -av  ./remote/ ./dump/
```

Load db-dump

```shell
mysql -u root -p audioasyl < ./dump/audioasyl.sql
```



#### Install Archiver

```shell
# create a virtualenv - python3.6 required 
virtualenv -p python3 ./venv
source ./venv/bin/activate

pip install -e git+https://github.com/ohrstrom/audioasyl-archiver.git
```


#### Run Archiver

```shell
# see:
archiver --help
# and
archiver archive --help

# example
archiver -v INFO archive \
-d ./data/out/ \
-s ./data/in \
-h mysql://root:root@localhost:3306/audioasyl \
playlist
```
