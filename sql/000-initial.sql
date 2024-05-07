--- Create web user qualificaiton
CREATE ROLE qualificaiton;
ALTER ROLE qualificaiton WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

--- Create DBA role
CREATE ROLE qualificaiton_dba;
ALTER ROLE qualificaiton_dba WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

CREATE TABLE deploy_releases
(
        version varchar(255),
        deployed_at timestamp default now()
);

ALTER TABLE deploy_releases OWNER TO qualificaiton_dba;

GRANT SELECT ON deploy_releases TO qualificaiton;

