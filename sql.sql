CREATE TABLE IF NOT EXISTS `courses`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `title` VARCHAR(255) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `courses_schedule`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `courses_id` INT NOT NULL DEFAULT -1,
   `times` VARCHAR(255) NOT NULL DEFAULT '',
   `capacity` INT NOT NULL DEFAULT -1,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Creative Cupcakes	Monday, 19:00; Wednesday, 19:00; Friday, 19:00	2
-- Digital Photography	Tuesday, 19:00; Thursday, 19:00	4
-- Family History for Beginners	Monday, 20:00; Tuesday, 20:00	3
-- Fundamentals of Acrylic Painting	Wednesday, 20:00; Friday, 20:00	2
-- Holiday French	Thursday, 20:00	2

INSERT INTO courses ( title ) VALUES ( "Creative Cupcakes");
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (1,"Monday, 19:00",2);
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (1,"Wednesday, 19:00",2);
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (1,"Friday, 19:00",2);

INSERT INTO courses ( title ) VALUES ( "Digital Photography");
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (2,"Tuesday, 19:00",4);
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (2,"Thursday, 19:00",4);

INSERT INTO courses ( title ) VALUES ( "Family History for Beginners");
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (3,"Monday, 20:00",3);
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (3,"Tuesday, 20:00",3);

INSERT INTO courses ( title ) VALUES ( "Fundamentals of Acrylic Painting");
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (4,"Wednesday, 20:00",2);
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (4,"Friday, 20:00",2); 

INSERT INTO courses ( title ) VALUES ( "Holiday French");
INSERT INTO courses_schedule ( courses_id, times,capacity) VALUES (5,"Thursday, 20:00",2);

 

CREATE TABLE IF NOT EXISTS `courses_records`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `courses_title` VARCHAR(255) NOT NULL DEFAULT '',
   `courses_times` VARCHAR(255) NOT NULL DEFAULT '',
   `user_name` VARCHAR(255) NOT NULL,
   `user_phone` VARCHAR(255) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;