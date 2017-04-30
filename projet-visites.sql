------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------



------------------------------------------------------------
-- Table: DOCTOR
------------------------------------------------------------
CREATE TABLE public.DOCTOR(
	idDoctor      SERIAL NOT NULL ,
	nameDoctor    VARCHAR (80) NOT NULL ,
	surnameDoctor VARCHAR (80) NOT NULL ,
	CONSTRAINT prk_constraint_DOCTOR PRIMARY KEY (idDoctor)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: EMPLOYEE
------------------------------------------------------------
CREATE TABLE public.EMPLOYEE(
	idEmployee      SERIAL NOT NULL ,
	nameEmployee    VARCHAR (80) NOT NULL ,
	surnameEmployee VARCHAR (80) NOT NULL ,
	admin           BOOL   ,
	CONSTRAINT prk_constraint_EMPLOYEE PRIMARY KEY (idEmployee)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: SPECIALTY
------------------------------------------------------------
CREATE TABLE public.SPECIALTY(
	idSpec  SERIAL NOT NULL ,
	libSpec VARCHAR (80) NOT NULL ,
	CONSTRAINT prk_constraint_SPECIALTY PRIMARY KEY (idSpec)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: APPOINTMENT
------------------------------------------------------------
CREATE TABLE public.APPOINTMENT(
	idAppoint      SERIAL NOT NULL ,
	dateHour       DATE  NOT NULL ,
	reportedStatus INT  NOT NULL ,
	CONSTRAINT prk_constraint_APPOINTMENT PRIMARY KEY (idAppoint)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: MEDIC
------------------------------------------------------------
CREATE TABLE public.MEDIC(
	idMedic   SERIAL NOT NULL ,
	libMedic  VARCHAR (80) NOT NULL ,
	descMedic VARCHAR (2000)  NOT NULL ,
	idRet     INT  NOT NULL ,
	CONSTRAINT prk_constraint_MEDIC PRIMARY KEY (idMedic)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: RETAILER
------------------------------------------------------------
CREATE TABLE public.RETAILER(
	idRet   SERIAL NOT NULL ,
	nameRet VARCHAR (80) NOT NULL ,
	CONSTRAINT prk_constraint_RETAILER PRIMARY KEY (idRet)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: ADDRESS
------------------------------------------------------------
CREATE TABLE public.ADDRESS(
	idAddr     SERIAL NOT NULL ,
	num        INT  NOT NULL ,
	street     VARCHAR (255) NOT NULL ,
	codePost   VARCHAR (10) NOT NULL ,
	city       VARCHAR (255) NOT NULL ,
	country    VARCHAR (255) NOT NULL ,
	indication VARCHAR (255) NOT NULL ,
	CONSTRAINT prk_constraint_ADDRESS PRIMARY KEY (idAddr)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: animates
------------------------------------------------------------
CREATE TABLE public.animates(
	idAppoint  INT  NOT NULL ,
	idEmployee INT  NOT NULL ,
	CONSTRAINT prk_constraint_animates PRIMARY KEY (idAppoint,idEmployee)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: is_prospected
------------------------------------------------------------
CREATE TABLE public.is_prospected(
	idDoctor  INT  NOT NULL ,
	idAppoint INT  NOT NULL ,
	CONSTRAINT prk_constraint_is_prospected PRIMARY KEY (idDoctor,idAppoint)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: has
------------------------------------------------------------
CREATE TABLE public.has(
	idDoctor INT  NOT NULL ,
	idSpec   INT  NOT NULL ,
	CONSTRAINT prk_constraint_has PRIMARY KEY (idDoctor,idSpec)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: is_mentioned
------------------------------------------------------------
CREATE TABLE public.is_mentioned(
	idMedic   INT  NOT NULL ,
	idAppoint INT  NOT NULL ,
	CONSTRAINT prk_constraint_is_mentioned PRIMARY KEY (idMedic,idAppoint)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: works_at
------------------------------------------------------------
CREATE TABLE public.works_at(
	idAddr   INT  NOT NULL ,
	idDoctor INT  NOT NULL ,
	CONSTRAINT prk_constraint_works_at PRIMARY KEY (idAddr,idDoctor)
)WITHOUT OIDS;



ALTER TABLE public.MEDIC ADD CONSTRAINT FK_MEDIC_idRet FOREIGN KEY (idRet) REFERENCES public.RETAILER(idRet);
ALTER TABLE public.animates ADD CONSTRAINT FK_animates_idAppoint FOREIGN KEY (idAppoint) REFERENCES public.APPOINTMENT(idAppoint);
ALTER TABLE public.animates ADD CONSTRAINT FK_animates_idEmployee FOREIGN KEY (idEmployee) REFERENCES public.EMPLOYEE(idEmployee);
ALTER TABLE public.is_prospected ADD CONSTRAINT FK_is_prospected_idDoctor FOREIGN KEY (idDoctor) REFERENCES public.DOCTOR(idDoctor);
ALTER TABLE public.is_prospected ADD CONSTRAINT FK_is_prospected_idAppoint FOREIGN KEY (idAppoint) REFERENCES public.APPOINTMENT(idAppoint);
ALTER TABLE public.has ADD CONSTRAINT FK_has_idDoctor FOREIGN KEY (idDoctor) REFERENCES public.DOCTOR(idDoctor);
ALTER TABLE public.has ADD CONSTRAINT FK_has_idSpec FOREIGN KEY (idSpec) REFERENCES public.SPECIALTY(idSpec);
ALTER TABLE public.is_mentioned ADD CONSTRAINT FK_is_mentioned_idMedic FOREIGN KEY (idMedic) REFERENCES public.MEDIC(idMedic);
ALTER TABLE public.is_mentioned ADD CONSTRAINT FK_is_mentioned_idAppoint FOREIGN KEY (idAppoint) REFERENCES public.APPOINTMENT(idAppoint);
ALTER TABLE public.works_at ADD CONSTRAINT FK_works_at_idAddr FOREIGN KEY (idAddr) REFERENCES public.ADDRESS(idAddr);
ALTER TABLE public.works_at ADD CONSTRAINT FK_works_at_idDoctor FOREIGN KEY (idDoctor) REFERENCES public.DOCTOR(idDoctor);
