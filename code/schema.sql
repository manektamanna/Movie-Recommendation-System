CREATE TABLE Genre (
Genre_id integer primary key,
Type varchar(128)
);

CREATE TABLE Theater_owner (
Owner_id integer primary key,
Age integer,
Name varchar (128)
);

CREATE TABLE Actors (
Actor_id integer primary key,
Age integer,
Name varchar (128), 
Language varchar (128),
Gender varchar(128)
);

CREATE TABLE Director (
Director_id integer primary key,
Age integer,
Name varchar (128), 
Language varchar (128),
Gender varchar(128)
);

CREATE TABLE Producers (
Producer_id integer primary key,
Age integer,
Name varchar (128), 
Language varchar (128),
Gender varchar(128)
);

CREATE TABLE Spectators (
Spectator_id integer primary key,
Age integer,
Name varchar (128), 
Language varchar (128),
Gender varchar(128)
);

CREATE TABLE Movie (
Movie_id integer primary key,
Movie_name varchar(128),
Movie_language varchar(128),
country varchar(128),
release_date integer,
Director_id integer not null,
FOREIGN KEY (Director_id) REFERENCES Director(Director_id)
);

CREATE TABLE Theater_owned_by (
Theater_id integer primary key, 
Theater_name varchar(128),
Theater_location varchar (128),
Owner_id integer not null,
FOREIGN KEY (Owner_id) REFERENCES Theater_owner (Owner_id) 
);

CREATE TABLE Shown_at (
Movie_id integer,
Theater_id integer, 
PRIMARY KEY (Movie_id, Theater_id), 
FOREIGN KEY (Movie_id) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Theater_id) REFERENCES Theater_owned_by (Theater_id) 
);

create table have_scenes(
Movie_Id integer,
Scene_Id integer,
Type varchar(128),
Timestamp integer,
PRIMARY KEY (Movie_id, Scene_id), 
FOREIGN KEY (Movie_id) REFERENCES Movie (Movie_id) on delete cascade 
);

CREATE TABLE Belong_to(
Movie_id integer,
Genre_id integer, 
PRIMARY KEY (Movie_id, Genre_id), 
FOREIGN KEY (Movie_id) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Genre_id) REFERENCES Genre (Genre_id) 
);

CREATE TABLE Receive_awards (
Year integer,
Type varchar (128), 
Movie_id integer not null,
Actor_id integer not null,
PRIMARY KEY (Year, type), 
FOREIGN KEY (Movie_id) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Actor_id) REFERENCES Actors (Actor_id) 
);

CREATE TABLE Produced_by (
Movie_id integer,
Producer_id integer, 
PRIMARY KEY (Movie_id, Producer_id), 
FOREIGN KEY (Movie_id) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Producer_id) REFERENCES Producers (Producer_id) 
);

CREATE TABLE Acted_by (
Movie_id integer,
Actor_id integer,
PRIMARY KEY (Movie_id, Actor_id), 
FOREIGN KEY (Movie_id) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Actor_id) REFERENCES Actors (Actor_id) 
);

CREATE TABLE Rated_by (
Movie_id integer,
Spectator_id integer,
Rating decimal,
PRIMARY KEY (Movie_id, Spectator_id), 
FOREIGN KEY (Movie_ID) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Spectator_id) REFERENCES Spectators (Spectator_id) 
);

CREATE TABLE Viewed_by (
Movie_id integer,
Spectator_id integer,
PRIMARY KEY (Movie_id, Spectator_id), 
FOREIGN KEY (Movie_ID) REFERENCES Movie (Movie_id), 
FOREIGN KEY (Spectator_id) REFERENCES Spectators (Spectator_id) 
);






