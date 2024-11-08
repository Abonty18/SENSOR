PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('2a5183a6df6d');
CREATE TABLE csv_file (
	id INTEGER NOT NULL, 
	filename VARCHAR(150) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO csv_file VALUES(1,'test.xlsx');
INSERT INTO csv_file VALUES(2,'test2.xlsx');
INSERT INTO csv_file VALUES(3,'test3.xlsx');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	department VARCHAR(50), 
	completed_courses VARCHAR(150), 
	experience_years INTEGER, 
	password VARCHAR(150) NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO user VALUES(1,'labiba','labiba@gmail.com',NULL,NULL,NULL,'sha256$GqlwbAdQjpOiOCke$8ba5cda1cbe6ec806fb165a43e5af8a35317d2240b7b996688a9c48d659a7349','Developer');
INSERT INTO user VALUES(2,'nabiha','nabiha@gmail.com',NULL,NULL,NULL,'sha256$KPhKo0JL055YLkYM$b7bb41a71c3d55c3c37220fefe1b756df092eaefd647edff68a7a5d6b729c29f','Annotator');
INSERT INTO user VALUES(3,'afraa','afraa@gmail.com',NULL,NULL,NULL,'sha256$7BiE0iLrpfZsUwmI$c6d29de8772cd729a18b2ecd9c7d47f6c7a7c65ad22412930b6335142cc2641d','Annotator');
INSERT INTO user VALUES(4,'sunef','sunef@gmail.com',NULL,NULL,NULL,'sha256$2buwGMuBGiOkvFJ9$bd7bb15ad976a81d03b71e7e9bae8ada70a3900ec1b0aa02e64b1899642edcec','Annotator');
INSERT INTO user VALUES(5,'rahim','rahim@gmail.com',NULL,NULL,NULL,'sha256$HrWo6VkEeiviMm2P$938fde9cd156c0af64aa2cb0d82ccd346e31e73dfdb879127a7de7a20bac5da9','Annotator');
INSERT INTO user VALUES(6,'rashida','rashidaprven@gmail.com',NULL,NULL,NULL,'sha256$JqYCMdDWFACijnUg$1805f83a63550717eec8549b9333e52d4bf43ea8257d619570832266dbe54401','Annotator');
INSERT INTO user VALUES(7,'papa','papa@gmail.com',NULL,NULL,NULL,'sha256$1k4KVgEZtKQU3ggy$c3a2399d535e1533c6e8bb348d2e2986f5ff71d1cdca1a8e01e5a3b5e6f90502','Annotator');
INSERT INTO user VALUES(8,'Abonty','abonty@gmail.com',NULL,NULL,NULL,'sha256$46Eeh6OX0DKvUxIv$1d21fb75dc355d41bd405d25fe7ab3259c4b0f29cae976419264c4a97c63878f','Developer');
INSERT INTO user VALUES(9,'Ridwan Kabir','ridwankabir@iut-dhaka.edu',NULL,NULL,NULL,'sha256$3xkKIZMOAI2iALUM$cc3d43af16298694f8353c90b531d59b2b1bcd6c3f7ff40de2d1ec0f760b03f9','Annotator');
INSERT INTO user VALUES(10,'Ridwan Kabir','mkabir.49367@gmail.com',NULL,NULL,NULL,'sha256$k3OQSlcCijgkZMOj$6686317d9b4ab685764952f422c4fa58a50db54fd5c818de606f2724844e5840','Developer');
CREATE TABLE annotation (
	id INTEGER NOT NULL, 
	review_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	annotation VARCHAR(50), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(review_id) REFERENCES review (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO annotation VALUES(1,1,2,'Privacy-Related Feature Request','2024-11-05 10:00:18.601317');
INSERT INTO annotation VALUES(2,2,2,'Privacy-Related Feature Request','2024-11-05 10:00:38.583771');
INSERT INTO annotation VALUES(3,2,2,'Privacy-Related Feature Request','2024-11-05 10:00:59.274968');
INSERT INTO annotation VALUES(4,1,2,'Privacy-Related Feature Request','2024-11-05 10:01:07.558799');
INSERT INTO annotation VALUES(5,3,2,'Privacy-Related Feature Request','2024-11-05 10:01:13.501519');
INSERT INTO annotation VALUES(6,4,2,'Privacy-Related Bug','2024-11-05 10:01:22.223800');
INSERT INTO annotation VALUES(7,5,2,'Privacy-Related Feature Request','2024-11-05 10:10:53.614907');
INSERT INTO annotation VALUES(8,6,2,NULL,'2024-11-05 10:10:57.540092');
INSERT INTO annotation VALUES(9,7,2,'Privacy-Related Bug','2024-11-05 10:43:28.796523');
INSERT INTO annotation VALUES(10,8,2,'Not Privacy-Related','2024-11-05 10:43:37.994617');
INSERT INTO annotation VALUES(11,9,2,'Privacy-Related Bug','2024-11-05 10:43:44.370240');
INSERT INTO annotation VALUES(12,10,3,'Privacy-Related Feature Request','2024-11-05 10:44:48.699925');
INSERT INTO annotation VALUES(13,11,3,'Privacy-Related Bug','2024-11-05 10:44:53.263582');
INSERT INTO annotation VALUES(14,12,3,'Privacy-Related Feature Request','2024-11-05 10:44:58.324416');
INSERT INTO annotation VALUES(15,13,4,'Privacy-Related Feature Request','2024-11-05 10:45:56.276082');
INSERT INTO annotation VALUES(16,14,4,'Not Privacy-Related','2024-11-05 10:46:04.448875');
INSERT INTO annotation VALUES(17,15,4,'Privacy-Related Bug','2024-11-06 06:10:36.158978');
INSERT INTO annotation VALUES(18,16,4,'Privacy-Related Bug','2024-11-06 06:10:47.033576');
INSERT INTO annotation VALUES(19,17,4,'Privacy-Related Bug','2024-11-06 06:22:16.764863');
INSERT INTO annotation VALUES(20,18,4,'Privacy-Related Bug','2024-11-06 06:24:02.509937');
INSERT INTO annotation VALUES(21,19,4,'Privacy-Related Feature Request+Bug','2024-11-06 06:24:07.770261');
INSERT INTO annotation VALUES(22,20,4,'Not Privacy-Related','2024-11-06 06:24:12.860975');
INSERT INTO annotation VALUES(23,22,5,'Privacy-Related Bug','2024-11-06 06:25:19.833810');
INSERT INTO annotation VALUES(24,23,5,'Not Privacy-Related','2024-11-06 06:25:24.088164');
INSERT INTO annotation VALUES(25,24,5,'Privacy-Related Feature Request','2024-11-06 06:25:28.303416');
INSERT INTO annotation VALUES(26,25,5,'Privacy-Related Bug','2024-11-06 06:25:33.138190');
INSERT INTO annotation VALUES(27,21,5,'Privacy-Related Feature Request+Bug','2024-11-06 06:36:10.730990');
INSERT INTO annotation VALUES(28,26,5,'Not Privacy-Related','2024-11-06 06:36:15.257271');
INSERT INTO annotation VALUES(29,27,5,'Privacy-Related Feature Request+Bug','2024-11-06 06:36:19.396747');
INSERT INTO annotation VALUES(30,29,4,'Privacy-Related Bug','2024-11-06 06:36:55.431705');
INSERT INTO annotation VALUES(31,30,4,'Privacy-Related Feature Request','2024-11-06 06:36:59.560450');
INSERT INTO annotation VALUES(32,3,4,'Privacy-Related Feature Request+Bug','2024-11-06 06:37:03.108047');
INSERT INTO annotation VALUES(33,28,2,'Privacy-Related Feature Request','2024-11-06 06:38:58.529946');
INSERT INTO annotation VALUES(34,5,2,'Privacy-Related Bug','2024-11-06 06:39:02.551735');
INSERT INTO annotation VALUES(35,6,2,'Not Privacy-Related','2024-11-06 06:39:08.226948');
INSERT INTO annotation VALUES(36,4,2,'Privacy-Related Feature Request','2024-11-06 07:17:00.393315');
INSERT INTO annotation VALUES(37,7,2,'Privacy-Related Bug','2024-11-06 07:17:04.727440');
INSERT INTO annotation VALUES(38,8,7,'Privacy-Related Bug','2024-11-06 07:19:38.207666');
INSERT INTO annotation VALUES(39,9,7,'Not Privacy-Related','2024-11-06 07:19:42.072778');
INSERT INTO annotation VALUES(40,10,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:19:46.743540');
INSERT INTO annotation VALUES(41,11,7,'Not Privacy-Related','2024-11-06 07:20:04.587595');
INSERT INTO annotation VALUES(42,12,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:20:08.144023');
INSERT INTO annotation VALUES(43,13,7,'Not Privacy-Related','2024-11-06 07:20:11.331966');
INSERT INTO annotation VALUES(44,14,7,'Not Privacy-Related','2024-11-06 07:20:15.859025');
INSERT INTO annotation VALUES(45,15,7,'Not Privacy-Related','2024-11-06 07:20:20.877839');
INSERT INTO annotation VALUES(46,16,7,'Not Privacy-Related','2024-11-06 07:20:31.356972');
INSERT INTO annotation VALUES(47,17,7,'Not Privacy-Related','2024-11-06 07:20:35.471205');
INSERT INTO annotation VALUES(48,18,7,'Not Privacy-Related','2024-11-06 07:20:39.386103');
INSERT INTO annotation VALUES(49,19,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:20:43.674152');
INSERT INTO annotation VALUES(50,20,7,'Not Privacy-Related','2024-11-06 07:20:48.592218');
INSERT INTO annotation VALUES(51,21,7,'Not Privacy-Related','2024-11-06 07:20:55.160075');
INSERT INTO annotation VALUES(52,22,7,'Not Privacy-Related','2024-11-06 07:21:02.513840');
INSERT INTO annotation VALUES(53,23,7,'Not Privacy-Related','2024-11-06 07:21:06.900702');
INSERT INTO annotation VALUES(54,24,7,'Privacy-Related Bug','2024-11-06 07:26:54.652771');
INSERT INTO annotation VALUES(55,25,7,'Not Privacy-Related','2024-11-06 07:26:58.325111');
INSERT INTO annotation VALUES(56,26,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:27:02.333290');
INSERT INTO annotation VALUES(57,27,7,'Not Privacy-Related','2024-11-06 07:27:06.074161');
INSERT INTO annotation VALUES(58,28,7,'Not Privacy-Related','2024-11-06 07:27:16.779526');
INSERT INTO annotation VALUES(59,29,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:27:20.605107');
INSERT INTO annotation VALUES(60,30,7,'Not Privacy-Related','2024-11-06 07:27:24.770789');
INSERT INTO annotation VALUES(61,1,7,'Not Privacy-Related','2024-11-06 07:27:28.634301');
INSERT INTO annotation VALUES(62,2,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:27:33.295964');
INSERT INTO annotation VALUES(63,3,7,'Privacy-Related Feature Request+Bug','2024-11-06 07:27:37.787543');
INSERT INTO annotation VALUES(64,4,7,'Not Privacy-Related','2024-11-06 07:27:42.233434');
INSERT INTO annotation VALUES(65,5,7,'Privacy-Related Bug','2024-11-06 07:29:06.359796');
INSERT INTO annotation VALUES(66,6,7,'Not Privacy-Related','2024-11-06 07:29:10.859485');
INSERT INTO annotation VALUES(67,7,7,'Privacy-Related Feature Request','2024-11-06 07:29:14.877288');
INSERT INTO annotation VALUES(68,8,7,'Not Privacy-Related','2024-11-06 07:29:23.080857');
INSERT INTO annotation VALUES(69,31,7,'Privacy-Related Feature Request+Bug','2024-11-06 10:33:18.675158');
INSERT INTO annotation VALUES(70,32,7,'Privacy-Related Feature Request+Bug','2024-11-06 10:33:21.506235');
INSERT INTO annotation VALUES(71,33,7,'Not Privacy-Related','2024-11-06 10:33:24.727879');
INSERT INTO annotation VALUES(72,9,9,'Privacy-Related Bug','2024-11-06 17:07:13.922315');
INSERT INTO annotation VALUES(73,10,9,'Not Privacy-Related','2024-11-06 17:07:28.415418');
INSERT INTO annotation VALUES(74,11,9,'Not Privacy-Related','2024-11-06 17:07:36.066967');
INSERT INTO annotation VALUES(75,34,9,'Privacy-Related Bug','2024-11-06 17:08:28.592720');
INSERT INTO annotation VALUES(76,51,9,'Not Privacy-Related','2024-11-06 17:11:29.265747');
INSERT INTO annotation VALUES(77,52,9,'Not Privacy-Related','2024-11-06 17:11:33.861312');
CREATE TABLE IF NOT EXISTS "completed_review" (
	id INTEGER NOT NULL, 
	annotator_1_id INTEGER, 
	annotation_1 TEXT, 
	annotator_2_id INTEGER, 
	annotation_2 TEXT, 
	annotator_3_id INTEGER, 
	annotation_3 TEXT, 
	completed_at DATETIME, 
	text TEXT NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_completed_review_annotator_1 FOREIGN KEY(annotator_1_id) REFERENCES user (id), 
	CONSTRAINT fk_completed_review_annotator_2 FOREIGN KEY(annotator_2_id) REFERENCES user (id), 
	CONSTRAINT fk_completed_review_annotator_3 FOREIGN KEY(annotator_3_id) REFERENCES user (id)
);
INSERT INTO completed_review VALUES(1,2,'Privacy-Related Feature Request',2,'Privacy-Related Feature Request',7,'Not Privacy-Related','2024-11-06 07:27:28.638288','Mark the spy');
INSERT INTO completed_review VALUES(2,2,'Privacy-Related Feature Request',2,'Privacy-Related Feature Request',7,'Privacy-Related Feature Request+Bug','2024-11-06 07:27:33.299511','Title');
INSERT INTO completed_review VALUES(3,2,'Privacy-Related Feature Request',4,'Privacy-Related Feature Request+Bug',7,'Privacy-Related Feature Request+Bug','2024-11-06 07:27:37.789984','My account says it’s been temporarily locked. I didn’t do anything to violate the rules against the app and when I’ve tried making a new account to use that one to contact my friends and family that account gets deleted as well. The app was working so well but it seems like there’s an update that was done that’s giving everyone this issue. I’ve tried contacting Snapchat’s support team as well and it was no use only to receive a page being told how this could of happened. It’s been 24 hours now and there is still no change at all. All of my memories are on that app from 2014 and now it’s all gone like that without even a notice. Snapchat please make a solution to this issue it’s ridiculous that we have to worry about not being able to access our personal information from this app. And please make a customer service phone number because trying to contact you guys is so darn difficult it’s not easy and it shouldn’t have to be that way. I’m sure many people can agree with me we need the app to be fixed as soon as possible !');
INSERT INTO completed_review VALUES(4,2,'Privacy-Related Bug',2,'Privacy-Related Feature Request',7,'Not Privacy-Related','2024-11-06 07:27:42.235761',replace('Put on your tin foil hats to deflect the mind control signal coming from the Illuminati! Mr. Zuck-a-burger is a giant lizard person trying to take control of you and your family!! Look at his evil snake eyes and reptilian smile. He may cry to try to impersonate emotions but those are really, in a literal sense, crocodile tears. Stop this crazed lunatic and big government busy bodies from bossing us around. Stop big capita, cancel cancel culture, and protect our personal data! God Bless Murica,\n Amen','\n',char(10)));
INSERT INTO completed_review VALUES(5,2,'Privacy-Related Feature Request',2,'Privacy-Related Bug',7,'Privacy-Related Bug','2024-11-06 07:29:06.362345',replace('I’m so sick and tired of us working our tails off to provide for ourselves. It becomes more and more obvious that we are slaves in this world, but we need to stop this we have Free Will and we need to make our own things and tell Society to piss off.\n\nMark Zuckerberg’s name means to spy on people and he was born in 1984, like Terminator 1984In the year 2026 artificial intelligence will have taken over as well the book George Orwell 1984.','\n',char(10)));
INSERT INTO completed_review VALUES(6,2,NULL,2,'Not Privacy-Related',7,'Not Privacy-Related','2024-11-06 07:29:10.861994','Couldn’t even set up my account because it got suspended automatically. Find, I say, I go to verify. Nope, there’s no way to get past the confirmation screen because the keyboard that you can’t dismiss covers the next button. Guess Zuckerberg is just going to have to miss out on my data.');
INSERT INTO completed_review VALUES(7,2,'Privacy-Related Bug',2,'Privacy-Related Bug',7,'Privacy-Related Feature Request','2024-11-06 07:29:14.880784','（该条评论已经被删除）They track and steal your data and information behind your back very personal things');
INSERT INTO completed_review VALUES(8,2,'Not Privacy-Related',7,'Privacy-Related Bug',7,'Not Privacy-Related','2024-11-06 07:29:23.083395',replace('Don’t you just love how a multibillion dollar company doesn’t have any support or call center… not like it would help, anyways.  \n\nI’ve found tons of bugs and ways to track who enters or “hacks” your account … but no one to address the issues and you lose photos of your mother who passed and birth photos and such you store on Facebook.\n\nI’ve tried again later… like it’s been years later.  Funny how easy it is to track contacts these days ….','\n',char(10)));
INSERT INTO completed_review VALUES(9,2,'Privacy-Related Bug',7,'Not Privacy-Related',9,'Privacy-Related Bug','2024-11-06 17:07:13.930414','I deleted the Facebook app months ago and somehow I still get notifications. Also, steals data and gives the user zero privacy.');
INSERT INTO completed_review VALUES(10,3,'Privacy-Related Feature Request',7,'Privacy-Related Feature Request+Bug',9,'Not Privacy-Related','2024-11-06 17:07:28.423440','Our data is collected and used/sold to other big companies that have data points on us.');
INSERT INTO completed_review VALUES(11,3,'Privacy-Related Bug',7,'Not Privacy-Related',9,'Not Privacy-Related','2024-11-06 17:07:36.072993','Social media in general can be dangerous. It steals our time and mines our data. Use with extreme caution.');
CREATE TABLE IF NOT EXISTS "review" (
	id INTEGER NOT NULL, 
	text TEXT NOT NULL, 
	annotation_count INTEGER, 
	created_at DATETIME, 
	csv_file_id INTEGER NOT NULL, 
	lock_time DATETIME, 
	in_progress_by INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_review_in_progress_by FOREIGN KEY(in_progress_by) REFERENCES user (id), 
	FOREIGN KEY(csv_file_id) REFERENCES csv_file (id)
);
INSERT INTO review VALUES(12,'No matter where you go, your feed, groups, marketplace, you’re never more than a few clicks away from being tricked by a stranger from a foreign country ready to steal your private info/money.  It’s amazing quite frankly that a billion dollar company cannot do anything about it.  If you have older relatives, get them off this platform now.  Every week a different friend gets compromised.  Marketplace is a total joke, opens your DMs to scammers plus tons of fake listings too.  Tried to sell a used suitcase once and got reported as misleading content.',2,'2024-11-05 09:58:58.692207',1,'2024-11-08 15:44:12.508710',7);
INSERT INTO review VALUES(13,'I’m so upset with Facebook right now!!! I logged out of my account and can’t log back in. I have tried all the ways suggested and still can’t get in. There’s no LIVE customer support to help you and the prompts suggested DONT work. This really bugs me because I’m locked out of my personal information.',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(14,'（该条评论已经被删除）Facebook should be a platform of free speech. Non-existent..If you’re against election fraud, abortion and even have opposing views about race and gender, you get flagged. Their fact checkers simply means to shut up because you cannot have an opinion that opposes their narrative. And instead, the platform discretely promotes hate, discrimination and manipulation.. the exact same things they said to be fighting against. And forget about privacy.. They monopolize every social platform so you are boxed in to using their product. They own Instagram, whatsapp, oculus vr, giphy, to name a few. Use them? Good luck.. They know everything about you. Remember, they make money selling your data. That’s a fact..  As the saying goes, if it’s free, YOU are the product.',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(15,'Facebook app won’t allow me to log on through the app. I tried logging out of all sessions and logging back in, i tried changing my password, I tried deleting the app and reinstalling it. Nothing works to allow me to log on through the app. I can still sign in using Safari, but still no access through the app.',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(16,'error fetching data always,why🤬🤬🤬🤬',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(17,'Facebook takes your information without your consent and uses it to fund left-wing , Marxist, and Chinese causes. It’s time to make it a public utility that’s accountable to the people!',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(18,'Mark this app is soul sucking delete and destroy',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(19,'Keep saying ERROR fetching DATA',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(20,'???',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(21,'No dark mode, settings is a labyrinth, so many ad permissions and tracking, privacy is a huge concern, not optimized for iPad',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(22,'He done zucced my data',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(23,'The new additions now makes you open sent reels from messenger into your url from phone app. This plan from this new add change is to gather more cookie and personal data on you and anyone else on your local network. It used to stay in app. Now it URL’s into my safari web browser app. Not cool Mark',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(24,'Hacked account apparently because my picture is showing but your not sending me the code to access',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(25,'I keep getting a fetching data message. It’s been days & I can’t use the app',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(26,'He’s done stole my personal data',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(27,'I’ve gotten banned twice a month and I haven’t even used this app much to share my opinion like I used to. I got banned for sharing a motivational quote with a male chest showing (working out) followed by a ban for trying to sell a post pregnancy girdle. It’s pathetic. There’s nothing you can do about it since you pay them with you private DATA, but have to accept their abuse without being able to appeal.',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(28,'I tried to report an inappropriate picture of a person clearly showing some private parts and yet, they tell me “it doesn’t go against our community guidelines”.',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(29,'When you are hacked they do nothing to help , no link no nothing . It’s like they helping people get there identity stolen',2,'2024-11-05 09:58:58.693200',1,NULL,NULL);
INSERT INTO review VALUES(30,'Two factor authentication is broken for months!!!! It won’t send the code to your cellphone and officially locks you out of your accounts… so basically all your data and connections are now theirs and theirs alone. Your only option is to create a “new” account which in turn falsely inflates their “user numbers”. This has to be criminal',2,'2024-11-05 09:58:58.694199',1,NULL,NULL);
INSERT INTO review VALUES(31,'Two factor authentication is broken for months!!!! It won’t send the code to your cellphone and officially locks you out of your accounts… so basically all your data and connections are now theirs and theirs alone. Your only option is to create a “new” account which in turn falsely inflates their “user numbers”. This has to be criminal',1,'2024-11-06 10:32:19.599928',2,NULL,NULL);
INSERT INTO review VALUES(32,'I had someone hack into my account and post pics of talaban.   So I have now been told that I did something against community standards.  If you can’t figure out that this was not me nor came from a source of mine then you need to stop your platform.  This is pathetic.  Facebook needs to sell to someone like Elon Musk',1,'2024-11-06 10:32:19.599928',2,NULL,NULL);
INSERT INTO review VALUES(33,'After the most recent January 2023 update, I’m unable to use the “finish watching” feature on my app. It keeps saying “there was an error fetching the data”. Ugh so frustrating! Fix it Facebook!',1,'2024-11-06 10:32:19.600950',2,NULL,NULL);
INSERT INTO review VALUES(34,'Why is my admin on a page taking over my personal page? I can’t access my linked pages or groups I’m in. What happened?',1,'2024-11-06 10:32:19.600950',2,NULL,NULL);
INSERT INTO review VALUES(35,'Uninstalled do to the constant nagging about wanting me to allow “personal ads” I’ll just use the web version which I recommend everyone does.',0,'2024-11-06 10:32:19.600950',2,NULL,NULL);
INSERT INTO review VALUES(36,'The latest update (Feb. 2023) is just rubbish. They’ve made switching between your page and personal profile an exercise in I May Not Care Enough Anymore. Are they trying to prevent people from wanting to use the app??',0,'2024-11-06 10:32:19.600950',2,NULL,NULL);
INSERT INTO review VALUES(37,'Sick of the tracking and things not working, spam adds, hacking!!!!  For what they make it should be 100%!!!',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(38,'The last business update is not user friendly. It is too difficult to keep my personal profile separate from by business page. It is so frustrating to have to keep bouncing back and forth.',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(39,'I’m tried if this app giving me data fetching error when I’m just trying to look through my news feed and watch videos',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(40,'Stop tracking me please 😿 ur making my dog cry.',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(41,'I’ve been hacked and can’t access my account.  The help center is no help at all, just a continuous loop of the same thing. No access to a live chat. I’m fed up!',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(42,'No deja actualizar la información personal ni laboral.',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(43,replace('Looks like the app doesn’t recognize my current password when I’m prompted to login again to access my account info.  And I’m hesitant to logout of the app completely (and back in again) to try to reset this for fear I’ll be locked out of the app until this bug is fixed!\n\nFYI, I did change my password via the website a few months ago, so the app *may* be recognizing the old password.','\n',char(10)),0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(44,'Invasion of privacy to your phone thats what this app is.',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(45,'You might as well forward your current location and personal information directly to the fbi 🙄',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(46,replace('I logged out of my Facebook days ago for personal reasons then when I’ve recently tried to log back in it gives me an error code that says I cannot login every time and this has been going on for days.\n\nI’ve tried drying and reinstalling, resetting my phone and more nothing works. I’ve never had a problem with Facebook but this is terrible especially when you use your account for business purposes.','\n',char(10)),0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(47,'I updated on the Facebook app and now I cannot see my personal Facebook nor my business Facebook this is why I hate updating',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(48,'This new update needs to be fixed I have had my Facebook account since 2007, I have a business page attach to my personal I cannot access both! Very frustrating',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(49,'Someone hacked my accounts. They removed my email and phone number. I’ve tried to get it back but there’s no help from Facebook.  They have control of my deceased husband’s memorial page, my photo page, and a page I’m an admin on. Facebook security is a joke.   I had the two factor authentication but when this person changed the phone number and email I couldn’t get in to use it.',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(50,'In the last 6 months Facebook business page has become a big hassle. I can’t toggle back and forth from my personal page easily.  Every function has become difficult to use. Please make it user friendly again.',0,'2024-11-06 10:32:19.602219',2,NULL,NULL);
INSERT INTO review VALUES(51,'Mark the spy',1,'2024-11-06 17:10:54.009036',3,NULL,NULL);
INSERT INTO review VALUES(52,'Title',1,'2024-11-06 17:10:54.010055',3,NULL,NULL);
INSERT INTO review VALUES(53,'My account says it’s been temporarily locked. I didn’t do anything to violate the rules against the app and when I’ve tried making a new account to use that one to contact my friends and family that account gets deleted as well. The app was working so well but it seems like there’s an update that was done that’s giving everyone this issue. I’ve tried contacting Snapchat’s support team as well and it was no use only to receive a page being told how this could of happened. It’s been 24 hours now and there is still no change at all. All of my memories are on that app from 2014 and now it’s all gone like that without even a notice. Snapchat please make a solution to this issue it’s ridiculous that we have to worry about not being able to access our personal information from this app. And please make a customer service phone number because trying to contact you guys is so darn difficult it’s not easy and it shouldn’t have to be that way. I’m sure many people can agree with me we need the app to be fixed as soon as possible !',0,'2024-11-06 17:10:54.010055',3,NULL,NULL);
INSERT INTO review VALUES(54,replace('Put on your tin foil hats to deflect the mind control signal coming from the Illuminati! Mr. Zuck-a-burger is a giant lizard person trying to take control of you and your family!! Look at his evil snake eyes and reptilian smile. He may cry to try to impersonate emotions but those are really, in a literal sense, crocodile tears. Stop this crazed lunatic and big government busy bodies from bossing us around. Stop big capita, cancel cancel culture, and protect our personal data! God Bless Murica,\n Amen','\n',char(10)),0,'2024-11-06 17:10:54.010055',3,NULL,NULL);
INSERT INTO review VALUES(55,replace('I’m so sick and tired of us working our tails off to provide for ourselves. It becomes more and more obvious that we are slaves in this world, but we need to stop this we have Free Will and we need to make our own things and tell Society to piss off.\n\nMark Zuckerberg’s name means to spy on people and he was born in 1984, like Terminator 1984In the year 2026 artificial intelligence will have taken over as well the book George Orwell 1984.','\n',char(10)),0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(56,'Couldn’t even set up my account because it got suspended automatically. Find, I say, I go to verify. Nope, there’s no way to get past the confirmation screen because the keyboard that you can’t dismiss covers the next button. Guess Zuckerberg is just going to have to miss out on my data.',0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(57,'（该条评论已经被删除）They track and steal your data and information behind your back very personal things',0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(58,replace('Don’t you just love how a multibillion dollar company doesn’t have any support or call center… not like it would help, anyways.  \n\nI’ve found tons of bugs and ways to track who enters or “hacks” your account … but no one to address the issues and you lose photos of your mother who passed and birth photos and such you store on Facebook.\n\nI’ve tried again later… like it’s been years later.  Funny how easy it is to track contacts these days ….','\n',char(10)),0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(59,'I deleted the Facebook app months ago and somehow I still get notifications. Also, steals data and gives the user zero privacy.',0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(60,'Our data is collected and used/sold to other big companies that have data points on us.',0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(61,'Social media in general can be dangerous. It steals our time and mines our data. Use with extreme caution.',0,'2024-11-06 17:10:54.011128',3,NULL,NULL);
INSERT INTO review VALUES(62,'No matter where you go, your feed, groups, marketplace, you’re never more than a few clicks away from being tricked by a stranger from a foreign country ready to steal your private info/money.  It’s amazing quite frankly that a billion dollar company cannot do anything about it.  If you have older relatives, get them off this platform now.  Every week a different friend gets compromised.  Marketplace is a total joke, opens your DMs to scammers plus tons of fake listings too.  Tried to sell a used suitcase once and got reported as misleading content.',0,'2024-11-06 17:10:54.012196',3,NULL,NULL);
INSERT INTO review VALUES(63,'I’m so upset with Facebook right now!!! I logged out of my account and can’t log back in. I have tried all the ways suggested and still can’t get in. There’s no LIVE customer support to help you and the prompts suggested DONT work. This really bugs me because I’m locked out of my personal information.',0,'2024-11-06 17:10:54.012196',3,NULL,NULL);
INSERT INTO review VALUES(64,'（该条评论已经被删除）Facebook should be a platform of free speech. Non-existent..If you’re against election fraud, abortion and even have opposing views about race and gender, you get flagged. Their fact checkers simply means to shut up because you cannot have an opinion that opposes their narrative. And instead, the platform discretely promotes hate, discrimination and manipulation.. the exact same things they said to be fighting against. And forget about privacy.. They monopolize every social platform so you are boxed in to using their product. They own Instagram, whatsapp, oculus vr, giphy, to name a few. Use them? Good luck.. They know everything about you. Remember, they make money selling your data. That’s a fact..  As the saying goes, if it’s free, YOU are the product.',0,'2024-11-06 17:10:54.012196',3,NULL,NULL);
INSERT INTO review VALUES(65,'Facebook app won’t allow me to log on through the app. I tried logging out of all sessions and logging back in, i tried changing my password, I tried deleting the app and reinstalling it. Nothing works to allow me to log on through the app. I can still sign in using Safari, but still no access through the app.',0,'2024-11-06 17:10:54.012196',3,NULL,NULL);
INSERT INTO review VALUES(66,'error fetching data always,why🤬🤬🤬🤬',0,'2024-11-06 17:10:54.012196',3,NULL,NULL);
INSERT INTO review VALUES(67,'Facebook takes your information without your consent and uses it to fund left-wing , Marxist, and Chinese causes. It’s time to make it a public utility that’s accountable to the people!',0,'2024-11-06 17:10:54.012196',3,NULL,NULL);
INSERT INTO review VALUES(68,'Mark this app is soul sucking delete and destroy',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(69,'Keep saying ERROR fetching DATA',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(70,'???',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(71,'No dark mode, settings is a labyrinth, so many ad permissions and tracking, privacy is a huge concern, not optimized for iPad',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(72,'He done zucced my data',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(73,'The new additions now makes you open sent reels from messenger into your url from phone app. This plan from this new add change is to gather more cookie and personal data on you and anyone else on your local network. It used to stay in app. Now it URL’s into my safari web browser app. Not cool Mark',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(74,'Hacked account apparently because my picture is showing but your not sending me the code to access',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(75,'I keep getting a fetching data message. It’s been days & I can’t use the app',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(76,'He’s done stole my personal data',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(77,'I’ve gotten banned twice a month and I haven’t even used this app much to share my opinion like I used to. I got banned for sharing a motivational quote with a male chest showing (working out) followed by a ban for trying to sell a post pregnancy girdle. It’s pathetic. There’s nothing you can do about it since you pay them with you private DATA, but have to accept their abuse without being able to appeal.',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(78,'I tried to report an inappropriate picture of a person clearly showing some private parts and yet, they tell me “it doesn’t go against our community guidelines”.',0,'2024-11-06 17:10:54.013191',3,NULL,NULL);
INSERT INTO review VALUES(79,'When you are hacked they do nothing to help , no link no nothing . It’s like they helping people get there identity stolen',0,'2024-11-06 17:10:54.014187',3,NULL,NULL);
INSERT INTO review VALUES(80,'Two factor authentication is broken for months!!!! It won’t send the code to your cellphone and officially locks you out of your accounts… so basically all your data and connections are now theirs and theirs alone. Your only option is to create a “new” account which in turn falsely inflates their “user numbers”. This has to be criminal',0,'2024-11-06 17:10:54.014187',3,NULL,NULL);
COMMIT;
