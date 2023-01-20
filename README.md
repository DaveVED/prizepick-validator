# prizepick-validator
API to pull down all Prize Pick projections for a given sport.

## Usage
To leverage this you can start the server and hit it via postman, curl, etc...

```
(.venv) dave@Davids-MBP prizepick-validator % uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/dave/workspace/github/personal/prizepick-validator']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [27021] using StatReload
INFO:     Started server process [27023]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

```
# http://127.0.0.1:8000/prizes/${leagueId}
curl http://127.0.0.1:8000/prizes/9
```

## League Ids
The following are valid League IDs.
9 -> NFL
