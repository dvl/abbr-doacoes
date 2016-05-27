# ABBR Doações

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
    
## Local

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

Copyright (C) André Luiz (contato@xdvl.info) - All Rights Reserved.

Unauthorized copying of this project, via any medium is strictly prohibited.

Proprietary and confidential.

* Your use of the item is restricted to a single installation.
* You may use the item in work which you are creating for your own purposes or for your client.
* You must not incorporate the item in a work which is created for redistribution or resale by you or your client.
* The item may not be redistributed or resold.
