#!/bin/bash
 
function init_db() {
    DB_DIR=db/
    DB_FILE=db/$1.db
    mkdir -p ${DB_DIR}
    touch ${DB_FILE}
}

function insert_features() {
    features=("$@")
    RET=()
    for i in "${features[@]}"
    do
        iid=`search_feature $i`
        if [ -z "$iid" ]; then
            echo $i >> $DB_FILE
            RET+=(`wc -l $DB_FILE | cut -f 1 -d ' '`)
        else
            RET+=($iid)
        fi
    done
}

function search_feature() {
    grep -n "^$1$" $DB_FILE | cut -f 1 -d ':'
}