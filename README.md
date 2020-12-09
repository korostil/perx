# perx
To start the app run `docker-compose up --build`

The app available on `http://0.0.0.0/`

Available URLs:
- login `POST api/users/login/ -d {"username": "ololo", "password": "ololo"}`
- logout `POST api/users/logout/`
- obtain token `POST api/users/token/`
- list of reports `GET api/analytics/reports/`
- create a report `POST api/analytics/reports/ -d {"file": "test.xlsx"}`
- get the report `GET api/analytics/reports/{id}/`
- delete the report `DELETE api/analytics/reports/{id}/`
- start processing the report `POST api/analytics/reports/{id}/start_processing/`
