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
CREATE TABLE systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
CREATE TABLE profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_id INTEGER NOT NULL,
            system_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (branch_id) REFERENCES branches(id),
            FOREIGN KEY (system_id) REFERENCES systems(id),
            UNIQUE(branch_id, system_id, name)
        );
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
CREATE TABLE requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            objet_demande TEXT NOT NULL,
            date_demande DATE NOT NULL,
            collaborator_type_id INTEGER,
            date_debut_stage DATE,
            date_fin_stage DATE,
            acces_partages TEXT,
            signature TEXT, status TEXT, responsable_id INTEGER, rejection_comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (collaborator_type_id) REFERENCES collaborator_types(id)
        );
INSERT INTO requests VALUES(1,2,'Octroi de nouveaux droits','2025-08-04',1,NULL,NULL,NULL,NULL,'soumis',4,NULL);
INSERT INTO requests VALUES(2,2,'Octroi de nouveaux droits','2025-08-04',1,NULL,NULL,NULL,NULL,'soumis',4,NULL);
INSERT INTO requests VALUES(3,2,'Modification - ajout','2025-08-05',1,NULL,NULL,NULL,NULL,'soumis',4,NULL);
CREATE TABLE branches_requests (
            request_id INTEGER NOT NULL,
            branch_id INTEGER NOT NULL,
            PRIMARY KEY (request_id, branch_id),
            FOREIGN KEY (request_id) REFERENCES requests(id),
            FOREIGN KEY (branch_id) REFERENCES branches(id)
        );
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
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('poles',5);
INSERT INTO sqlite_sequence VALUES('departments',5);
INSERT INTO sqlite_sequence VALUES('users',5);
INSERT INTO sqlite_sequence VALUES('collaborator_types',1);
INSERT INTO sqlite_sequence VALUES('requests',3);
INSERT INTO sqlite_sequence VALUES('network_accesses',3);
INSERT INTO sqlite_sequence VALUES('request_history',3);
COMMIT;
