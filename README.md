# Fipe Collector

Fipe Collector is an application designed to collect vehicles data from the brazilian organization "Tabela Fipe". This project is been built in Python (Flask), Vue.js and MySQL. 


## Features

* Migrate database
* Collect vehicle's brands
* Collect vehicle's models
* Collect vehicle's versions


## Installation and usage

Gunicorn server is started by docker-compose, frontend is running inside python server, there is a configuration for dev environment and another for production.

To start dev environment, run `docker-compose up` at application's root folder. 

Application will be running at port 7002, backend apis are accessible by routes starting with /api.



## License

The Fipe Collector application is licensed under the terms of the GPL Open Source license and is available for free.
