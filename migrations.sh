#!/bin/bash
if ! command -v sqlite3 2>&1 >/dev/null
then
    echo "sqlite3 could not be found"
    exit 1
fi

if [ ! -f ./data/gbd.db ]; then
	sqlite3 ./data/gbd.db <<EOF
CREATE TABLE IF NOT EXISTS "gbd_ng" (
  "id" INTEGER PRIMARY KEY,
  "Sex" TEXT,
  "date_of_birth" DATE,
  "Weight" INTEGER,
  "Height" INTEGER,
  'WBC' REAL, 
  'RBC' REAL, 
  'HGB' REAL, 
  'HCT' REAL, 
  'PLT' REAL, 
  'PCT' REAL, 
  'MPV' REAL, 
  'MCV' REAL,
  'MCH' REAL, 
  'MCHC' REAL, 
  'PDW' REAL, 
  'RDW' REAL, 
  'RDW_SD' REAL, 
  'RDW_CV' REAL, 
  'LY_REL' REAL, 
  'MO_REL' REAL, 
  'NE_REL' REAL, 
  'EO_REL' REAL,
  'BA_REL' REAL, 
  'COLOR_INDEX' REAL, 
  'LY_ABS' REAL, 
  'MO_ABS' REAL, 
  'NE_ABS' REAL, 
  'EO_ABS' REAL, 
  'BA_ABS' REAL, 
  'BAND_NEUT' REAL,
  'SEGM_NEUT' REAL, 
  'LY_LEICO' REAL, 
  'MO_LEICO' REAL, 
  'EO_LEICO' REAL, 
  'BA_LEICO' REAL, 
  'ESR_Westergren' REAL
);
CREATE INDEX "ix_gbd_ng_index"ON "gbd_ng" ("id");
EOF
else 
	echo "./data/gbd.db already exist"
fi

