#!/bin/sh
export PGUSER="postgres"

psql -c "CREATE DATABASE project"

psql project -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

psql project -c "CREATE SCHEMA project_schema"
psql project -c "CREATE SCHEMA project_management_schema"
psql project -c "ALTER DATABASE project SET search_path TO project_schema, project_management_schema"