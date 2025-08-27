PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE poles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
INSERT INTO poles VALUES(1,'azeazez');
INSERT INTO poles VALUES(2,'non');
INSERT INTO poles VALUES(3,'oui');
INSERT INTO poles VALUES(4,'lo');
INSERT INTO poles VALUES(5,'me');
CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pole_id INTEGER NOT NULL,
            FOREIGN KEY (pole_id) REFERENCES poles(id)
        );
INSERT INTO departments VALUES(1,'azeaz',1);
INSERT INTO departments VALUES(2,'non',2);
INSERT INTO departments VALUES(3,'oui',3);
INSERT INTO departments VALUES(4,'lo',4);
INSERT INTO departments VALUES(5,'me',5);
CREATE TABLE branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
INSERT INTO branches VALUES(1,'AUTO');
INSERT INTO branches VALUES(2,'IARDS');
INSERT INTO branches VALUES(3,'Transport');
INSERT INTO branches VALUES(4,'Santé');
INSERT INTO branches VALUES(5,'Epargne');
INSERT INTO branches VALUES(6,'Prévoyance');
INSERT INTO branches VALUES(7,'Comptabilité');
INSERT INTO branches VALUES(8,'Recouvrement');
INSERT INTO branches VALUES(9,'RH');
CREATE TABLE systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
INSERT INTO systems VALUES(1,'SIEBEL');
INSERT INTO systems VALUES(2,'SAP');
INSERT INTO systems VALUES(3,'INTRANET');
CREATE TABLE profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_id INTEGER NOT NULL,
            system_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (branch_id) REFERENCES branches(id),
            FOREIGN KEY (system_id) REFERENCES systems(id),
            UNIQUE(branch_id, system_id, name)
        );
INSERT INTO profiles VALUES(1,1,1,'Gestionnaire AUTO');
INSERT INTO profiles VALUES(2,1,1,'Responsable AUTO');
INSERT INTO profiles VALUES(3,1,1,'Consultant AUTO');
INSERT INTO profiles VALUES(4,1,2,'Comptable AUTO');
INSERT INTO profiles VALUES(5,1,2,'Chef de projet AUTO');
INSERT INTO profiles VALUES(6,1,2,'Auditeur AUTO');
INSERT INTO profiles VALUES(7,1,3,'Utilisateur AUTO');
INSERT INTO profiles VALUES(8,1,3,'Administrateur AUTO');
INSERT INTO profiles VALUES(9,1,3,'Lecteur AUTO');
INSERT INTO profiles VALUES(10,2,1,'Gestionnaire IARDS');
INSERT INTO profiles VALUES(11,2,1,'Responsable IARDS');
INSERT INTO profiles VALUES(12,2,1,'Consultant IARDS');
INSERT INTO profiles VALUES(13,2,2,'Comptable IARDS');
INSERT INTO profiles VALUES(14,2,2,'Chef de projet IARDS');
INSERT INTO profiles VALUES(15,2,2,'Auditeur IARDS');
INSERT INTO profiles VALUES(16,2,3,'Utilisateur IARDS');
INSERT INTO profiles VALUES(17,2,3,'Administrateur IARDS');
INSERT INTO profiles VALUES(18,2,3,'Lecteur IARDS');
INSERT INTO profiles VALUES(19,3,1,'Gestionnaire Transport');
INSERT INTO profiles VALUES(20,3,1,'Responsable Transport');
INSERT INTO profiles VALUES(21,3,1,'Consultant Transport');
INSERT INTO profiles VALUES(22,3,2,'Comptable Transport');
INSERT INTO profiles VALUES(23,3,2,'Chef de projet Transport');
INSERT INTO profiles VALUES(24,3,2,'Auditeur Transport');
INSERT INTO profiles VALUES(25,3,3,'Utilisateur Transport');
INSERT INTO profiles VALUES(26,3,3,'Administrateur Transport');
INSERT INTO profiles VALUES(27,3,3,'Lecteur Transport');
INSERT INTO profiles VALUES(28,4,1,'Gestionnaire Santé');
INSERT INTO profiles VALUES(29,4,1,'Responsable Santé');
INSERT INTO profiles VALUES(30,4,1,'Consultant Santé');
INSERT INTO profiles VALUES(31,4,2,'Comptable Santé');
INSERT INTO profiles VALUES(32,4,2,'Chef de projet Santé');
INSERT INTO profiles VALUES(33,4,2,'Auditeur Santé');
INSERT INTO profiles VALUES(34,4,3,'Utilisateur Santé');
INSERT INTO profiles VALUES(35,4,3,'Administrateur Santé');
INSERT INTO profiles VALUES(36,4,3,'Lecteur Santé');
INSERT INTO profiles VALUES(37,5,1,'Gestionnaire Epargne');
INSERT INTO profiles VALUES(38,5,1,'Responsable Epargne');
INSERT INTO profiles VALUES(39,5,1,'Consultant Epargne');
INSERT INTO profiles VALUES(40,5,2,'Comptable Epargne');
INSERT INTO profiles VALUES(41,5,2,'Chef de projet Epargne');
INSERT INTO profiles VALUES(42,5,2,'Auditeur Epargne');
INSERT INTO profiles VALUES(43,5,3,'Utilisateur Epargne');
INSERT INTO profiles VALUES(44,5,3,'Administrateur Epargne');
INSERT INTO profiles VALUES(45,5,3,'Lecteur Epargne');
INSERT INTO profiles VALUES(46,6,1,'Gestionnaire Prévoyance');
INSERT INTO profiles VALUES(47,6,1,'Responsable Prévoyance');
INSERT INTO profiles VALUES(48,6,1,'Consultant Prévoyance');
INSERT INTO profiles VALUES(49,6,2,'Comptable Prévoyance');
INSERT INTO profiles VALUES(50,6,2,'Chef de projet Prévoyance');
INSERT INTO profiles VALUES(51,6,2,'Auditeur Prévoyance');
INSERT INTO profiles VALUES(52,6,3,'Utilisateur Prévoyance');
INSERT INTO profiles VALUES(53,6,3,'Administrateur Prévoyance');
INSERT INTO profiles VALUES(54,6,3,'Lecteur Prévoyance');
INSERT INTO profiles VALUES(55,7,1,'Gestionnaire Comptabilité');
INSERT INTO profiles VALUES(56,7,1,'Responsable Comptabilité');
INSERT INTO profiles VALUES(57,7,1,'Consultant Comptabilité');
INSERT INTO profiles VALUES(58,7,2,'Comptable Comptabilité');
INSERT INTO profiles VALUES(59,7,2,'Chef de projet Comptabilité');
INSERT INTO profiles VALUES(60,7,2,'Auditeur Comptabilité');
INSERT INTO profiles VALUES(61,7,3,'Utilisateur Comptabilité');
INSERT INTO profiles VALUES(62,7,3,'Administrateur Comptabilité');
INSERT INTO profiles VALUES(63,7,3,'Lecteur Comptabilité');
INSERT INTO profiles VALUES(64,8,1,'Gestionnaire Recouvrement');
INSERT INTO profiles VALUES(65,8,1,'Responsable Recouvrement');
INSERT INTO profiles VALUES(66,8,1,'Consultant Recouvrement');
INSERT INTO profiles VALUES(67,8,2,'Comptable Recouvrement');
INSERT INTO profiles VALUES(68,8,2,'Chef de projet Recouvrement');
INSERT INTO profiles VALUES(69,8,2,'Auditeur Recouvrement');
INSERT INTO profiles VALUES(70,8,3,'Utilisateur Recouvrement');
INSERT INTO profiles VALUES(71,8,3,'Administrateur Recouvrement');
INSERT INTO profiles VALUES(72,8,3,'Lecteur Recouvrement');
INSERT INTO profiles VALUES(73,9,1,'Gestionnaire RH');
INSERT INTO profiles VALUES(74,9,1,'Responsable RH');
INSERT INTO profiles VALUES(75,9,1,'Consultant RH');
INSERT INTO profiles VALUES(76,9,2,'Comptable RH');
INSERT INTO profiles VALUES(77,9,2,'Chef de projet RH');
INSERT INTO profiles VALUES(78,9,2,'Auditeur RH');
INSERT INTO profiles VALUES(79,9,3,'Utilisateur RH');
INSERT INTO profiles VALUES(80,9,3,'Administrateur RH');
INSERT INTO profiles VALUES(81,9,3,'Lecteur RH');
CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department_id INTEGER,
            pole_id INTEGER,
            password TEXT NOT NULL, role TEXT,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (pole_id) REFERENCES poles(id)
        );
INSERT INTO users VALUES(1,'erezrze','zerzerze','harounriahi905@gmail.com',1,1,'scrypt:32768:8:1$U3J82rhIYTyt3XQM$86e2ca73d9e1ba7230af01191f0a66246f3036c44060a660991c1047e7fcd521171d6e08d981407bd0a50c537e25c9c468f7edc90cc8f25316d4340c318ac352',NULL);
INSERT INTO users VALUES(2,'linda','sahbeni','hariahi@ucm.es',2,2,'scrypt:32768:8:1$HXJMn5KgZDyuH6TK$7da36d18996a75dd67f7b50ae87f6f77103f9541fabc4c07a79f40d3fe12856a0bf40d7ceb96bfb17fb15354e157823c71a88ff31383b2b047b999a2ad2ac6fe','informatique');
INSERT INTO users VALUES(3,'amine','ferjeni','haroun.riahi@hotmail.com',3,3,'scrypt:32768:8:1$izKHhChgGI125X4i$281f43f0ffe47a2a99d4897f60338b19d0605a2557ce9cd4fe617b79925578c3876f53d5e4a754e791c3a5b4dbee1fe6eec19c7d8c52c8e2b4c19b9a6f03ecd8','validateur');
INSERT INTO users VALUES(4,'maher','ayechi','haroun.riiahii@gmail.com',4,4,'scrypt:32768:8:1$goNjolH7VrxYpSJB$2caa4ae54a121a75c8980300efda504b1226b806d381e7ea247f4d7594586b3346c21ac503fe85e173e5fda29728d587a62e3e5ef44d6265ff69622316605bd1','responsable');
INSERT INTO users VALUES(5,'arij','drissi','harounriahi60@gmail.com',5,5,'scrypt:32768:8:1$EI6gPzCVzbrrNXgq$97f64d80ea390ec2196b1c49b357b8ef1a1d7974ab00025fd4651b9a22210a21bb023eb2d5eede55e94e29050c92f1ed9c09256bcd333fe2dccab3fa6c02fade','informatique');
CREATE TABLE collaborator_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
INSERT INTO collaborator_types VALUES(1,'interne');
INSERT INTO collaborator_types VALUES(2,'externe');
INSERT INTO collaborator_types VALUES(3,'stagiaire');
CREATE TABLE requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            objet_demande TEXT NOT NULL,
            date_demande DATE NOT NULL,
            collaborator_type_id INTEGER,
            date_debut_stage DATE,
            date_fin_stage DATE,
            acces_partages TEXT,
            signature TEXT, status TEXT, responsable_id INTEGER, rejection_comment TEXT, departement TEXT, pole TEXT, nom_complet TEXT, matricule TEXT, email TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (collaborator_type_id) REFERENCES collaborator_types(id)
        );
INSERT INTO requests VALUES(1,2,'Octroi de nouveaux droits','2025-08-04',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(2,2,'Octroi de nouveaux droits','2025-08-04',1,NULL,NULL,NULL,NULL,'validé',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(3,2,'Modification - ajout','2025-08-05',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(4,2,'Octroi de nouveaux droits','2025-08-06',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(5,3,'Modification - suppression','2025-08-06',2,NULL,NULL,NULL,NULL,'cloturée',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(6,2,'Modification - ajout','2025-08-06',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(7,2,'Octroi de nouveaux droits','2025-08-06',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(8,2,'Modification - ajout','2025-08-07',1,NULL,NULL,NULL,NULL,'validé',4,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO requests VALUES(9,2,'Mutation','2025-08-07',1,NULL,NULL,NULL,NULL,'soumis',4,NULL,'khatafouni','inik khatafouni','amr diab','95555','amrdiab@gmail.com');
INSERT INTO requests VALUES(10,2,'Octroi de nouveaux droits','2025-08-07',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,'mmamamaam','ùmamamam','mamama','mamama','mamam@ucm.es');
INSERT INTO requests VALUES(11,2,'Départ','2025-08-07',1,NULL,NULL,NULL,NULL,'soumis',4,NULL,'i want it i got it','i see it i like it ','ariana grande','97','ariana@gmail.com');
INSERT INTO requests VALUES(12,2,'Modification - ajout','2025-08-07',1,NULL,NULL,NULL,NULL,'soumis',4,NULL,'parapapapa','parapapa','papier ','20029','papier@gmail.com');
INSERT INTO requests VALUES(13,2,'Octroi de nouveaux droits','2025-08-07',1,NULL,NULL,'enta habibi habibi habibi ana',NULL,'cloturée',4,NULL,'mamamam','papapa','papap','222222','haroun@gmail.com');
INSERT INTO requests VALUES(14,2,'Octroi de nouveaux droits','2025-08-07',1,NULL,NULL,'non',NULL,'cloturée',4,NULL,'informatique','info','haroun riahi','20000','haroun@gmail.com');
INSERT INTO requests VALUES(15,2,'Octroi de nouveaux droits','2025-08-07',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,'sdfdgf','dfgdfg','dfgdfgf','dfgdfgdf','erfzer@hotmail.com');
INSERT INTO requests VALUES(16,2,'Octroi de nouveaux droits','2025-08-07',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,'zerzer','jahaz','zerzer','zerzerzr','hazuzeg@ucm.es');
INSERT INTO requests VALUES(17,2,'Octroi de nouveaux droits','2025-08-20',1,NULL,NULL,NULL,NULL,'cloturée',4,NULL,'droit','droit','malek mah','13121','malek@gmail.com');
INSERT INTO requests VALUES(18,2,'Modification - suppression','2025-08-20',3,'2025-08-09','2025-08-23','pres',NULL,'cloturée',4,NULL,'assurance','vie','mahmoud','131221121','mahmoud@gmail.com');
CREATE TABLE branches_requests (
            request_id INTEGER NOT NULL,
            branch_id INTEGER NOT NULL,
            PRIMARY KEY (request_id, branch_id),
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (branch_id) REFERENCES branches(id)
        );
INSERT INTO branches_requests VALUES(11,1);
INSERT INTO branches_requests VALUES(11,2);
INSERT INTO branches_requests VALUES(12,1);
INSERT INTO branches_requests VALUES(13,5);
INSERT INTO branches_requests VALUES(13,7);
INSERT INTO branches_requests VALUES(14,1);
INSERT INTO branches_requests VALUES(14,5);
INSERT INTO branches_requests VALUES(15,1);
INSERT INTO branches_requests VALUES(15,4);
INSERT INTO branches_requests VALUES(16,1);
INSERT INTO branches_requests VALUES(16,6);
INSERT INTO branches_requests VALUES(17,2);
INSERT INTO branches_requests VALUES(18,2);
INSERT INTO branches_requests VALUES(18,5);
CREATE TABLE request_system_profiles (
            request_id INTEGER NOT NULL,
            system_id INTEGER NOT NULL,
            profile_id INTEGER NOT NULL,
            environment TEXT NOT NULL CHECK(environment IN ('TEST', 'PROD')),
            PRIMARY KEY (request_id, system_id, profile_id, environment),
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (system_id) REFERENCES systems(id),
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        );
INSERT INTO request_system_profiles VALUES(12,3,7,'TEST');
INSERT INTO request_system_profiles VALUES(12,3,8,'PROD');
INSERT INTO request_system_profiles VALUES(12,3,9,'TEST');
INSERT INTO request_system_profiles VALUES(12,2,4,'TEST');
INSERT INTO request_system_profiles VALUES(12,2,5,'TEST');
INSERT INTO request_system_profiles VALUES(12,2,6,'TEST');
INSERT INTO request_system_profiles VALUES(12,1,1,'PROD');
INSERT INTO request_system_profiles VALUES(12,1,2,'TEST');
INSERT INTO request_system_profiles VALUES(12,1,3,'TEST');
INSERT INTO request_system_profiles VALUES(13,3,43,'TEST');
INSERT INTO request_system_profiles VALUES(13,3,44,'TEST');
INSERT INTO request_system_profiles VALUES(13,3,45,'PROD');
INSERT INTO request_system_profiles VALUES(13,1,37,'TEST');
INSERT INTO request_system_profiles VALUES(13,1,38,'TEST');
INSERT INTO request_system_profiles VALUES(13,1,39,'PROD');
INSERT INTO request_system_profiles VALUES(13,3,61,'PROD');
INSERT INTO request_system_profiles VALUES(13,3,62,'PROD');
INSERT INTO request_system_profiles VALUES(13,3,63,'TEST');
INSERT INTO request_system_profiles VALUES(13,2,58,'TEST');
INSERT INTO request_system_profiles VALUES(13,2,59,'TEST');
INSERT INTO request_system_profiles VALUES(13,2,60,'TEST');
INSERT INTO request_system_profiles VALUES(13,1,55,'PROD');
INSERT INTO request_system_profiles VALUES(13,1,56,'TEST');
INSERT INTO request_system_profiles VALUES(13,1,57,'TEST');
INSERT INTO request_system_profiles VALUES(14,3,7,'TEST');
INSERT INTO request_system_profiles VALUES(14,3,8,'PROD');
INSERT INTO request_system_profiles VALUES(14,3,9,'TEST');
INSERT INTO request_system_profiles VALUES(14,3,45,'TEST');
INSERT INTO request_system_profiles VALUES(14,2,41,'TEST');
INSERT INTO request_system_profiles VALUES(14,1,38,'PROD');
INSERT INTO request_system_profiles VALUES(15,3,7,'TEST');
INSERT INTO request_system_profiles VALUES(15,3,8,'PROD');
INSERT INTO request_system_profiles VALUES(15,3,9,'TEST');
INSERT INTO request_system_profiles VALUES(15,1,3,'TEST');
INSERT INTO request_system_profiles VALUES(15,1,29,'TEST');
INSERT INTO request_system_profiles VALUES(16,3,7,'TEST');
INSERT INTO request_system_profiles VALUES(16,3,8,'TEST');
INSERT INTO request_system_profiles VALUES(16,3,9,'PROD');
INSERT INTO request_system_profiles VALUES(16,3,54,'TEST');
INSERT INTO request_system_profiles VALUES(16,1,48,'PROD');
INSERT INTO request_system_profiles VALUES(17,3,16,'TEST');
INSERT INTO request_system_profiles VALUES(17,3,17,'PROD');
INSERT INTO request_system_profiles VALUES(17,3,18,'TEST');
INSERT INTO request_system_profiles VALUES(17,2,13,'TEST');
INSERT INTO request_system_profiles VALUES(17,2,14,'TEST');
INSERT INTO request_system_profiles VALUES(17,2,15,'TEST');
INSERT INTO request_system_profiles VALUES(17,1,12,'PROD');
INSERT INTO request_system_profiles VALUES(18,3,16,'TEST');
INSERT INTO request_system_profiles VALUES(18,3,17,'PROD');
INSERT INTO request_system_profiles VALUES(18,3,18,'TEST');
INSERT INTO request_system_profiles VALUES(18,2,13,'TEST');
INSERT INTO request_system_profiles VALUES(18,2,14,'TEST');
INSERT INTO request_system_profiles VALUES(18,2,40,'PROD');
INSERT INTO request_system_profiles VALUES(18,2,42,'TEST');
CREATE TABLE network_accesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
INSERT INTO network_accesses VALUES(1,'messagerie');
INSERT INTO network_accesses VALUES(2,'internet');
INSERT INTO network_accesses VALUES(3,'session');
CREATE TABLE request_network_accesses (
            request_id INTEGER NOT NULL,
            network_access_id INTEGER NOT NULL,
            PRIMARY KEY (request_id, network_access_id),
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (network_access_id) REFERENCES network_accesses(id)
        );
INSERT INTO request_network_accesses VALUES(1,1);
INSERT INTO request_network_accesses VALUES(2,2);
INSERT INTO request_network_accesses VALUES(3,2);
INSERT INTO request_network_accesses VALUES(3,3);
INSERT INTO request_network_accesses VALUES(4,2);
INSERT INTO request_network_accesses VALUES(4,1);
INSERT INTO request_network_accesses VALUES(5,2);
INSERT INTO request_network_accesses VALUES(5,1);
INSERT INTO request_network_accesses VALUES(5,3);
INSERT INTO request_network_accesses VALUES(6,3);
INSERT INTO request_network_accesses VALUES(7,3);
INSERT INTO request_network_accesses VALUES(8,1);
INSERT INTO request_network_accesses VALUES(9,2);
INSERT INTO request_network_accesses VALUES(10,2);
INSERT INTO request_network_accesses VALUES(10,1);
INSERT INTO request_network_accesses VALUES(10,3);
INSERT INTO request_network_accesses VALUES(11,1);
INSERT INTO request_network_accesses VALUES(12,1);
INSERT INTO request_network_accesses VALUES(13,2);
INSERT INTO request_network_accesses VALUES(13,1);
INSERT INTO request_network_accesses VALUES(13,3);
INSERT INTO request_network_accesses VALUES(14,2);
INSERT INTO request_network_accesses VALUES(14,1);
INSERT INTO request_network_accesses VALUES(15,1);
INSERT INTO request_network_accesses VALUES(16,2);
INSERT INTO request_network_accesses VALUES(16,1);
INSERT INTO request_network_accesses VALUES(17,1);
INSERT INTO request_network_accesses VALUES(18,2);
INSERT INTO request_network_accesses VALUES(18,1);
INSERT INTO request_network_accesses VALUES(18,3);
CREATE TABLE request_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            actor_id INTEGER,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (actor_id) REFERENCES users(id)
        );
INSERT INTO request_history VALUES(1,1,'soumis',2,NULL,'2025-08-04 11:00:30');
INSERT INTO request_history VALUES(2,2,'soumis',2,NULL,'2025-08-04 12:21:37');
INSERT INTO request_history VALUES(3,3,'soumis',2,NULL,'2025-08-05 13:34:42');
INSERT INTO request_history VALUES(4,3,'clôturée',2,NULL,'2025-08-06 10:32:33');
INSERT INTO request_history VALUES(5,1,'clôturée',2,NULL,'2025-08-06 10:32:43');
INSERT INTO request_history VALUES(6,2,'validé',2,'','2025-08-06 10:35:20');
INSERT INTO request_history VALUES(7,4,'soumis',2,NULL,'2025-08-06 10:38:20');
INSERT INTO request_history VALUES(8,4,'validé',2,'','2025-08-06 10:38:42');
INSERT INTO request_history VALUES(9,4,'clôturée',2,NULL,'2025-08-06 10:38:49');
INSERT INTO request_history VALUES(10,5,'soumis',3,NULL,'2025-08-06 11:19:32');
INSERT INTO request_history VALUES(11,5,'validé',3,'','2025-08-06 11:20:43');
INSERT INTO request_history VALUES(12,5,'clôturée',2,NULL,'2025-08-06 11:21:15');
INSERT INTO request_history VALUES(13,6,'soumis',2,NULL,'2025-08-06 11:42:53');
INSERT INTO request_history VALUES(14,6,'validé',2,'','2025-08-06 11:43:11');
INSERT INTO request_history VALUES(15,6,'clôturée',2,NULL,'2025-08-06 11:43:20');
INSERT INTO request_history VALUES(16,7,'soumis',2,NULL,'2025-08-06 12:15:28');
INSERT INTO request_history VALUES(17,7,'validé',2,'','2025-08-06 12:15:58');
INSERT INTO request_history VALUES(18,7,'clôturée',2,NULL,'2025-08-06 12:16:03');
INSERT INTO request_history VALUES(19,8,'soumis',2,NULL,'2025-08-07 08:28:48');
INSERT INTO request_history VALUES(20,9,'soumis',2,NULL,'2025-08-07 08:49:35');
INSERT INTO request_history VALUES(21,10,'soumis',2,NULL,'2025-08-07 09:04:45');
INSERT INTO request_history VALUES(22,10,'validé',2,'','2025-08-07 09:09:25');
INSERT INTO request_history VALUES(23,10,'clôturée',2,NULL,'2025-08-07 09:09:27');
INSERT INTO request_history VALUES(24,10,'validé',2,'','2025-08-07 09:09:29');
INSERT INTO request_history VALUES(25,10,'clôturée',2,NULL,'2025-08-07 09:09:30');
INSERT INTO request_history VALUES(26,11,'soumis',2,NULL,'2025-08-07 09:49:42');
INSERT INTO request_history VALUES(27,12,'soumis',2,NULL,'2025-08-07 10:08:03');
INSERT INTO request_history VALUES(28,13,'soumis',2,NULL,'2025-08-07 10:09:38');
INSERT INTO request_history VALUES(29,13,'validé',2,'','2025-08-07 10:46:51');
INSERT INTO request_history VALUES(30,13,'clôturée',2,NULL,'2025-08-07 10:47:46');
INSERT INTO request_history VALUES(31,14,'soumis',2,NULL,'2025-08-07 11:11:06');
INSERT INTO request_history VALUES(32,14,'validé',2,'','2025-08-07 11:18:12');
INSERT INTO request_history VALUES(33,14,'clôturée',2,NULL,'2025-08-07 11:18:18');
INSERT INTO request_history VALUES(34,15,'soumis',2,NULL,'2025-08-07 11:33:47');
INSERT INTO request_history VALUES(35,15,'validé',2,'','2025-08-07 11:34:14');
INSERT INTO request_history VALUES(36,15,'clôturée',2,NULL,'2025-08-07 11:34:28');
INSERT INTO request_history VALUES(37,16,'soumis',2,NULL,'2025-08-07 11:52:09');
INSERT INTO request_history VALUES(38,16,'validé',2,'','2025-08-07 11:53:13');
INSERT INTO request_history VALUES(39,16,'clôturée',2,NULL,'2025-08-07 11:53:19');
INSERT INTO request_history VALUES(40,8,'validé',2,'','2025-08-14 10:02:32');
INSERT INTO request_history VALUES(41,17,'soumis',2,NULL,'2025-08-20 07:44:04');
INSERT INTO request_history VALUES(42,17,'validé',2,'','2025-08-20 07:44:21');
INSERT INTO request_history VALUES(43,17,'traité',2,NULL,'2025-08-20 07:59:40');
INSERT INTO request_history VALUES(44,17,'clôturée',2,NULL,'2025-08-20 08:03:15');
INSERT INTO request_history VALUES(45,18,'soumis',2,NULL,'2025-08-20 08:14:02');
INSERT INTO request_history VALUES(46,18,'validé',2,'','2025-08-20 08:14:32');
INSERT INTO request_history VALUES(47,18,'validé',2,'','2025-08-20 08:15:15');
INSERT INTO request_history VALUES(48,18,'traité',2,NULL,'2025-08-20 08:16:17');
INSERT INTO request_history VALUES(49,18,'clôturée',2,NULL,'2025-08-20 08:16:30');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('poles',5);
INSERT INTO sqlite_sequence VALUES('departments',5);
INSERT INTO sqlite_sequence VALUES('users',5);
INSERT INTO sqlite_sequence VALUES('collaborator_types',3);
INSERT INTO sqlite_sequence VALUES('requests',18);
INSERT INTO sqlite_sequence VALUES('network_accesses',3);
INSERT INTO sqlite_sequence VALUES('request_history',49);
INSERT INTO sqlite_sequence VALUES('branches',9);
INSERT INTO sqlite_sequence VALUES('systems',3);
INSERT INTO sqlite_sequence VALUES('profiles',81);
COMMIT;
