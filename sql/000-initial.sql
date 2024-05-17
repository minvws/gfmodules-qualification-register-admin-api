--- Create web user qualificaiton
CREATE ROLE qualification;
ALTER ROLE qualificaton WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

--- Create DBA role
CREATE ROLE qualificaton_dba;
ALTER ROLE qualificaton_dba WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

CREATE TABLE deploy_releases
(
        version varchar(255),
        deployed_at timestamp default now()
);

ALTER TABLE deploy_releases OWNER TO qualificaton_dba;

GRANT SELECT ON deploy_releases TO qualificaton;;

