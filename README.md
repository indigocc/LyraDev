# LyraDev

This project provides a simple chat engine backed by a MariaDB database.

## Environment variables

`MemoryStore` reads its database connection settings from the following
environment variables. Each has a sensible default if not provided.

- `DB_HOST` - database host (default `10.1.1.5`)
- `DB_PORT` - database port (default `3307`)
- `DB_USER` - database username (default `lyra`)
- `DB_PASSWORD` - database password (default `Lyra_PW4321`)
- `DB_DATABASE` - database name (default `lyra_memory`)

Define these variables before running the application if you need to override
the defaults.
