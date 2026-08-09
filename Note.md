[x]Delete all migration/versions , create a new migration to fix SQLite->Postgres

[x]set database URL  in `.env `file  from `SQLALCHEMY_DATABASE_URL = sqlite:///./sqlite.db` to `SQLALCHEMY_DATABASE_URL = postgresql://postgres:<username>@localhost:<port>/<db-name>`

-- TODO --
[ ] multistage docker build.

[ ] redis cache.

[ ] fix variable suitable name and change variable name to standard.

[ ] UI/UX .
