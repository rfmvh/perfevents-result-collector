--
-- experiments
--
DROP SEQUENCE IF EXISTS exp_id_seq CASCADE;
CREATE SEQUENCE exp_id_seq INCREMENT 1 START 1;

DROP TABLE IF EXISTS experiments CASCADE;
CREATE TABLE experiments (
	exp_id INTEGER NOT NULL DEFAULT nextval('exp_id_seq') PRIMARY KEY,
	cmd VARCHAR(256),
	description VARCHAR(256),
	systemwide BOOLEAN NOT NULL DEFAULT FALSE,
	name VARCHAR(64) NOT NULL);
ALTER SEQUENCE exp_id_seq OWNED BY experiments.exp_id;

--
-- tools
--
DROP SEQUENCE IF EXISTS tool_id_seq CASCADE;
CREATE SEQUENCE tool_id_seq INCREMENT 1 START 1;

DROP TABLE IF EXISTS tools CASCADE;
CREATE TABLE tools (
	tool_id INTEGER NOT NULL DEFAULT nextval('tool_id_seq') PRIMARY KEY,
	name VARCHAR(32) NOT NULL,
	version VARCHAR(32) NOT NULL);
ALTER SEQUENCE tool_id_seq OWNED BY tools.tool_id;


--
-- virt
--
DROP SEQUENCE IF EXISTS virt_id_seq CASCADE;
CREATE SEQUENCE virt_id_seq INCREMENT 1 START 1;

DROP TABLE IF EXISTS virt CASCADE;
CREATE TABLE virt (
	virt_id INTEGER NOT NULL DEFAULT nextval('virt_id_seq') PRIMARY KEY,
	name VARCHAR(16) NOT NULL);
ALTER SEQUENCE virt_id_seq OWNED BY virt.virt_id;

--
-- kernels
--
DROP SEQUENCE IF EXISTS kernel_id_seq CASCADE;
CREATE SEQUENCE kernel_id_seq INCREMENT 1 START 10000;

DROP TABLE IF EXISTS kernels CASCADE;
CREATE TABLE kernels (
	kernel_id INTEGER NOT NULL DEFAULT nextval('kernel_id_seq') PRIMARY KEY,
	name VARCHAR(32) NOT NULL);
ALTER SEQUENCE kernel_id_seq OWNED BY kernels.kernel_id;

--
-- environments
--
DROP SEQUENCE IF EXISTS env_id_seq CASCADE;
CREATE SEQUENCE env_id_seq INCREMENT 1 START 1000000;

DROP TABLE IF EXISTS environments CASCADE;
CREATE TABLE environments (
	env_id INTEGER NOT NULL DEFAULT nextval('env_id_seq') PRIMARY KEY,
	arch VARCHAR(16) NOT NULL,
	microarch VARCHAR(32) NOT NULL,
	family INTEGER,
	model INTEGER,
	stepping INTEGER,
	virt_id INTEGER NOT NULL REFERENCES virt(virt_id),
	kernel_id INTEGER NOT NULL REFERENCES kernels(kernel_id));
ALTER SEQUENCE env_id_seq OWNED BY environments.env_id;

--
-- events
--
DROP SEQUENCE IF EXISTS event_id_seq CASCADE;
CREATE SEQUENCE event_id_seq INCREMENT 1 START 1000000;

DROP TABLE IF EXISTS events CASCADE;
CREATE TABLE events (
	event_id INTEGER NOT NULL DEFAULT nextval('event_id_seq') PRIMARY KEY,
	name VARCHAR(64) NOT NULL,
	evt_num INTEGER,
	nmask INTEGER,
	idgroup INTEGER NOT NULL);
ALTER SEQUENCE event_id_seq OWNED BY events.event_id;

--
-- results
--
DROP SEQUENCE IF EXISTS rsl_id_seq CASCADE;
CREATE SEQUENCE rsl_id_seq INCREMENT 1 START 10000000;

DROP TABLE IF EXISTS results CASCADE;
CREATE TABLE results (
	rsl_id INTEGER NOT NULL DEFAULT nextval('rsl_id_seq') PRIMARY KEY,
	exp_id INTEGER NOT NULL REFERENCES experiments(exp_id),
	tool_id INTEGER NOT NULL REFERENCES tools(tool_id),
	env_id INTEGER NOT NULL REFERENCES environments(env_id),
	event_id INTEGER NOT NULL REFERENCES events(event_id),
	val FLOAT NOT NULL,
	reliability_manual FLOAT,
	reliability_auto FLOAT);
ALTER SEQUENCE rsl_id_seq OWNED BY results.rsl_id;
