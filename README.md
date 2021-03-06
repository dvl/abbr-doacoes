# ABBR Doações [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dvl/abbr-doacoes)

Sistema para coleta de doação para ABBR.

# Instalação

Para instalar e rodar o projeto você vai precisar:

Da forma fácil:

* Docker
* docker-compose

Da maneira manual:

* Python 3.5+
* PostgreSQL
* bower

## Docker

    $ make install
    $ make up
    
## Manual

    $ sudo -u postgres createdb abbr
    $ cp .env-example .env
    $ vim .env
    $ mkvirtualenv --python=`which python3` abbr
    $ pip install -r requirements.txt
    $ bower install
    $ python manage.py migrate
    $ python manage.py runserver
    
Após a instalação você poderá acessar o site para desenvolvimento em [http://localhost:8000/]()

# Licença

MIT
