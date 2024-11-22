#!/bin/bash
if ! command -v sqlite3 2>&1 >/dev/null
then
    echo "sqlite3 could not be found"
	sudo apt install sqlite3
    exit 1
fi

if [ ! -f ./gbd.db ]; then
	sqlite3 gbd.db <<EOF
CREATE TABLE IF NOT EXISTS "gbd_ng" (
  "id" INTEGER PRIMARY KEY,
  "gender" TEXT,
  "date_of_birth" DATE,
  "height" INTEGER,
  "weight" INTEGER,
  "mcv" REAL,
  "mch" REAL,
  "mchc" REAL,
  "ly_abs" REAL,
  "mo_abs" REAL,
  "ne_abs" REAL,
  "eo_abs" REAL,
  "ba_abs" REAL
);
CREATE INDEX "ix_gbd_ng_index"ON "gbd_ng" ("id");
EOF
else 
	echo "./gbd.db already exist"
fi

