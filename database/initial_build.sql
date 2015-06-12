/*This is a sql script to do the initial database build and import the usda
data from their .csv files.  This is a build specifically
for Django: all tables have surrogate id's as per Django's requirements.

Build process is as follows:
1. build schema (this file)
2. import data (this file)
3. add 'id' columns that django expects to see (this file)
4. hand over control to Django:
   # python manage.py makemigrations usdarest
   # python manage.py migrate

note: - foreign keys are managed by Django 
      - these 6 tables have "managed=False" set in models.py
      - this schema isn't finalized and the project may even move to
        manually parsing the csv's and importing them using the ORM
        due to the long-term difficulties of unmanaged tables.*/


/* Food Description, 8,618 records */
create table usda_food_desc(
       food_id		    CHAR(5)      primary key,
       food_group_id 	CHAR(4)      not null,
       long_desc 	    VARCHAR(200) not null,
       short_desc 	    VARCHAR(200) not null,
       common_name 	    VARCHAR(100),
       manufacture_name VARCHAR(65),
       survey  		    CHAR(1),
       refuse_desc 	    VARCHAR(135),
       refuse 		    NUMERIC(2,0),
       scientific_name 	VARCHAR(65),
       n_factor 	    NUMERIC(4,2),
       pro_factor 	    NUMERIC(4,2),
       fat_factor 	    NUMERIC(4,2),
       cho_factor 	    NUMERIC(4,2)
);


/* Food Group Description, 25 records */
create table usda_food_group(
       food_group_id	CHAR(4)  primary key,
       food_group_desc 	CHAR(60) not null
);


/* Nutrient Data, 654,572 records */
create table usda_nutrient_data(
       food_id		     CHAR(5)       not null,
       nutr_id 		     CHAR(3)       not null,
       nutr_value 	     NUMERIC(10,3) not null,
       num_data_pts 	 NUMERIC(5,0)  not null,
       std_error 	     NUMERIC(8,3),
       source_code 	     CHAR(2)       not null,
       derivation_code 	 CHAR(4),
       ref_food_id 	     CHAR(5),
       fortified 	     CHAR(1),
       number_studies 	 NUMERIC(2,0),
       min_value 	     NUMERIC(10,3),
       max_value 	     NUMERIC(10,3),
       degrees_freedom 	 NUMERIC(4,0),
       low_error_bound 	 NUMERIC(10,3),
       upper_error_bound NUMERIC(10,3),
       statistical_cmt 	 CHAR(10),
       addmod_date 	     CHAR(10),
       confidence_code 	 CHAR(1),
       unique (food_id, nutr_id)
);
/* ^^^ "id SERIAL" is added to this table after the data is imported. */


/* Nutrient Definition, 150 records */
create table usda_nutrient_def(
       nutr_id		    CHAR(3)      primary key,
       units 		    VARCHAR(7)   not null,
       tagname 		    VARCHAR(20),
       nutr_desc 	    VARCHAR(60)  not null,
       decimal_places 	CHAR(1)      not null,   /* USDA has this as alphanumeric? */
       sr_order 	    NUMERIC(6,0) not null
);


/* Weight, 15,228 records */
create table usda_weight(
       food_id		    CHAR(5),
       seq 		        CHAR(2),
       amount 		    NUMERIC(5,3) not null,
       measure_desc 	VARCHAR(84)  not null,
       grams 		    NUMERIC(7,1) not null,
       num_data_pts 	NUMERIC(4,0),
       std_dev 		    NUMERIC(7,3),
       unique (food_id, Seq)
);
/* ^^^ "id SERIAL" is also added to this table after the data is imported" */



/* Import all the data.  File paths are relative to current working directory. */
\copy usda_food_desc      FROM 'database/sr27asc/FOOD_DES.txt' (FORMAT CSV, DELIMITER '^', QUOTE '~', encoding 'latin1');
\copy usda_food_group     FROM 'database/sr27asc/FD_GROUP.txt' (FORMAT CSV, DELIMITER '^', QUOTE '~', encoding 'latin1');
\copy usda_nutrient_data  FROM 'database/sr27asc/NUT_DATA.txt' (FORMAT CSV, DELIMITER '^', QUOTE '~', encoding 'latin1');
\copy usda_nutrient_def   FROM 'database/sr27asc/NUTR_DEF.txt' (FORMAT CSV, DELIMITER '^', QUOTE '~', encoding 'latin1');
\copy usda_weight         FROM 'database/sr27asc/WEIGHT.txt'   (FORMAT CSV, DELIMITER '^', QUOTE '~', encoding 'latin1');


/* Add the id fields as surrogate keys to tables that would have composite primary
keys per django's requirements.  Composite keys are enforced as together_unique
 in Django's ORM'*/
alter table usda_nutrient_data add column id serial;
update usda_nutrient_data set id = default;
alter table usda_nutrient_data add primary key (id);

alter table usda_weight add column id serial;
update usda_weight set id = default;
alter table usda_weight add primary key (id);
