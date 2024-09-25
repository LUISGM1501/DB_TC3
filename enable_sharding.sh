#!/bin/bash

mongosh --eval '
sh.enableSharding("myTravelDB");
sh.shardCollection("myTravelDB.usuarios", { "username": "hashed" });
'
