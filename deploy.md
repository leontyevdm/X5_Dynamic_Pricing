**Как задеплоить **

*Тут будет рассматриваться установка с свежей только что установленной CentOS 7*

1) Включить Интернет https://lintut.com/how-to-setup-network-after-rhelcentos-7-minimal-installation/
2) Установить гит - `sudo yum install git`
3) Клонируем репозиторий `git clone <url>`, на момент написания этого документа url=http://bb.prac.atp-fivt.org:8080/scm/xdp/pricing.git
4) Переходим в папку проекта `cd pricing`
5) `sudo yum install epel-release`
6) Нам нужен питон третьей версии - `sudo yum install python36`
7) `sudo yum install python36-pip python36-devel gcc nginx`
8) `sudo pip3 install virtualenv`
9) Для того, чтобы не засорять глобальный неймспейс создаем виртуальное окружение конкретно для нашего проекта `virtualenv venv`
12) Активируем окружение `source venv/bin/activate` справа от командной строки появится `(venv)`
13) `git checkout <нужная ветка>` - если вам нужен код не с main, на данный момент backend-XDP-40
14) `pip3 install -r requirements.txt`  
15) `uwsgi --workers <workers> --threads <threads> --socket <ip_address>:<port> --protocol=http -w main --pyargv <port>`, где `<ip_address>` - ip адрес сервера, `<port>` - порт, на который будут приходить сигналы, `<workers>` - количество процессов, советуем ставить столько же, сколько ядер на сервере, `<threads>` - количество потоков, аналогично


*Теперь работает? 0_0*