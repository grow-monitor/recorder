# grow-recorder-service

A service to continuously record sensor data from an MQTT Broker

## Dependencies

- `psycopg2` has a dependency on `pg_config`, which you can install by running `sudo apt install libpq-dev` (Debian / Ubuntu).

## Recording as a service

- Copy `service/grow-recorder.service.example` to `service/grow-recorder.service` and fill in the blanks.
- Run `./service/install.sh` to install the recorder as a background task.
