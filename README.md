# Eartquakes challenge
System that uses USGS Earthquakes public data set to show relevant info about earthquakes and cities.

## Dataset
https://earthquake.usgs.gov/earthquakes/search/

## Used Stack
```
Docker          v20.10.21
Docker Compose  v2.13.0
```
Main tech used: Python, Mysql, SqlAlchemy, Pandas, FastAPI, GeoPy


## Local Setup
``` bash
$ docker-compose up
```

## Database migration
TODO


## Makefile
Contains helpful commands used in everyday life.

## Implementation
``` bash
./config/       # Config / Infrastructure (e.g, database)
./exceptions/   # Custom exceptions
./integration/  # Integration with external systems (third parties or public data)
./models/       # Database models (e.g., SQLAlchemy models)
./routers/      # Router instance and routes
./schemas/      # Data "schemas" (e.g., Pydantic models)
./services/     # Business logic
app.py          # Main app
```

## Cache Solution
`requests_cache` is a Python package that allows to cache API responses effortlessly. It transparently intercepts and stores API responses, reducing redundant requests and enhancing performance. It offers flexible caching strategies and supports different storage backends. Integration is easy, requiring minimal code changes. By caching API responses, it optimizes applications with rate limits, large response sizes, or slow servers.

## API Documentation / Swagger
`FastAPI`, a Python web framework, provides built-in support for automatic API documentation generation using `Swagger`. Swagger UI allows developers to explore and test APIs through an interactive and user-friendly interface. With FastAPI's type hints and intuitive decorators, API endpoints and models are automatically documented, including request/response models, headers, and status codes. The Swagger UI can be accessed via a dedicated endpoint, providing comprehensive documentation and an API playground. This built-in feature saves time and effort, ensuring accurate and up-to-date API documentation that aids in API consumption and integration by developers.

http://localhost:8000/docs


## Postman
`Postman` is a popular API development and testing tool that simplifies the process of working with APIs. It provides an intuitive interface for making API requests, organizing and managing collections, and automating tests, making it a valuable tool for developers and testers.

TODO: add url
Since we don't have relevant/sensitive information at Postman, I'm sharing the collection here.
In a real environment, we would have an shared environment with the team to collaborate.


## Tests
TODO


## Next Steps / TODO:
- refac service: https://camillovisini.com/article/abstracting-fastapi-services/
- exception handler : https://fastapi.tiangolo.com/tutorial/handling-errors/
- create response / swagger documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/
- unit tests
- alembic
- black/PEP8
- authentication