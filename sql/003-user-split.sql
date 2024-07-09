-- Split users
REVOKE ALL ON TABLE deploy_releases FROM qualification;
DROP ROLE qualification;

CREATE ROLE qualification_admin;
ALTER ROLE qualification_admin WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

CREATE ROLE qualification_api;
ALTER ROLE qualification_api WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS ;

GRANT SELECT ON deploy_releases TO qualification_admin;
GRANT SELECT ON deploy_releases TO qualification_api;


GRANT SELECT,INSERT,UPDATE,DELETE ON vendors TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON protocols TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON protocol_versions TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON roles TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON system_types TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON applications TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON application_versions TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON healthcare_providers TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON applications_roles TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON applications_types TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON healthcare_providers_application_versions TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON healthcare_providers_qualifications TO qualification_admin;
GRANT SELECT,INSERT,UPDATE,DELETE ON protocol_application_qualifications TO qualification_admin;
GRANT SELECT ON vendors TO qualification_api;
GRANT SELECT ON protocols TO qualification_api;
GRANT SELECT ON protocol_versions TO qualification_api;
GRANT SELECT ON roles TO qualification_api;
GRANT SELECT ON system_types TO qualification_api;
GRANT SELECT ON applications TO qualification_api;
GRANT SELECT ON application_versions TO qualification_api;
GRANT SELECT ON healthcare_providers TO qualification_api;
GRANT SELECT ON applications_roles TO qualification_api;
GRANT SELECT ON applications_types TO qualification_api;
GRANT SELECT ON healthcare_providers_application_versions TO qualification_api;
GRANT SELECT ON healthcare_providers_qualifications TO qualification_api;
GRANT SELECT ON protocol_application_qualifications TO qualification_api;
