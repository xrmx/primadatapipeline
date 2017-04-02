#!/bin/sh

luigi --module pipeline StoreData --date $1 --local-scheduler
