-- create vendors table and triggers
CREATE TABLE vendors (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    kvk_number VARCHAR(50) NOT NULL UNIQUE,
    trade_name VARCHAR(150) NOT NULL,
    statutory_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id)
);

/*
  as specified in the architecture document, see:
  https://github.com/minvws/nl-irealisatie-zmodules-process-internal/blob/metadata-register/architectuur/kwalificatieregister.md#protocol
*/
-- create Protocols table with types and triggers
CREATE TYPE protocol_type as ENUM('InformationStandard', 'Directive');

CREATE TABLE protocols (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    protocol_type protocol_type NOT NULL,
    name VARCHAR(150) NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id)
);

-- create ProtocolVersions table with types and triggers
CREATE TABLE protocol_versions (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    version VARCHAR(50) NOT NULL,
    description VARCHAR,
    protocol_id uuid NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id),
    CONSTRAINT protocols_versions_protocols_fk FOREIGN KEY (protocol_id) REFERENCES protocols (id) ON DELETE CASCADE
);

-- create Roles table with triggers
CREATE TABLE roles (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL UNIQUE,
    description VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id)
);

-- create SystemTypes table with triggers
CREATE TABLE system_types (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id)
);

-- create Applications table with triggers
CREATE TABLE applications (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    vendor_id uuid NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id),
    UNIQUE (id, name),
    CONSTRAINT applications_vendors_fk FOREIGN KEY (vendor_id) REFERENCES vendors (id) ON DELETE CASCADE
);

-- create ApplicationVersions table with triggers
CREATE TABLE application_versions (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    version VARCHAR(50) NOT NULL,
    application_id uuid NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id),
    CONSTRAINT applications_versions_application_fk FOREIGN KEY (application_id) REFERENCES applications (id) ON DELETE CASCADE
);

-- create HealthcareProvider table with triggers
CREATE TABLE healthcare_providers (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    ura_code VARCHAR(50) NOT NULL UNIQUE,
    agb_code VARCHAR(50) NOT NULL UNIQUE,
    trade_name VARCHAR(150) NOT NULL,
    statutory_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    PRIMARY KEY (id)
);

-- create Applications junction table with Roles
CREATE TABLE applications_roles (
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE, -- Probably not needed
    application_id uuid REFERENCES applications (id) ON UPDATE CASCADE ON DELETE CASCADE,
    role_id uuid REFERENCES roles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    CONSTRAINT applications_roles_pk PRIMARY KEY (application_id, role_id)
);

-- create Applications junction table with SystemTypes
CREATE TABLE applications_types (
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE, -- Probably not needed
    application_id uuid REFERENCES applications (id) ON UPDATE CASCADE ON DELETE CASCADE,
    system_type_id uuid REFERENCES system_types (id) ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    CONSTRAINT applications_types_pk PRIMARY KEY(application_id, system_type_id)
);

-- create HealthcareProvider junction table with ApplicationVersions
CREATE TABLE healthcare_providers_application_versions (
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE, -- Probably not needed
    healthcare_provider_id uuid REFERENCES healthcare_providers (id) ON UPDATE CASCADE ON DELETE CASCADE,
    application_version_id uuid REFERENCES application_versions (id) ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    CONSTRAINT healthcare_providers_application_versions_pk PRIMARY KEY (healthcare_provider_id, application_version_id)
);

-- create Qualifications junction table between HealthcareProviders and ProtocolVersions
CREATE TABLE healthcare_providers_qualifications(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE, -- Probably not needed
    healthcare_provider_id uuid REFERENCES healthcare_providers (id) ON UPDATE CASCADE ON DELETE CASCADE,
    protocol_version_id uuid REFERENCES protocol_versions (id) ON UPDATE CASCADE ON DELETE CASCADE,
    qualification_date DATE NOT NULL,
    archived_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    CONSTRAINT healthcare_providers_qualifications_pk PRIMARY KEY (healthcare_provider_id, protocol_version_id)
);

-- create Qualifications junction table between ApplicationVersion and ProtocolVersions
CREATE TABLE protocol_application_qualifications(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE, -- Probably not needed
    application_version_id uuid REFERENCES application_versions (id) ON UPDATE CASCADE ON DELETE CASCADE,
    protocol_version_id uuid REFERENCES protocol_versions (id) ON UPDATE CASCADE ON DELETE CASCADE,
    qualification_date DATE NOT NULL,
    archived_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    modified_at TIMESTAMP default NOW(),

    CONSTRAINT protocol_application_qualifications_pk PRIMARY KEY (application_version_id, protocol_version_id)
);
