# hakaton_blood_classification

## usage:
```
apt install sqlite3
./migrations.sh
pip install - r requirements.txt
```
## changes
moved to form 
redirect to result page on submit button 
moved storage to sqlite backend with sqlalchemy 
## usage 
to list all reports use:
```
sqlite3 gbd.db 'select * from gbd_ng;'
```
## todo
- check db schema 
- add unnecessary columns to schema 
- actual processing
