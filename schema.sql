CREATE TYPE STATUS AS ENUM ('enabled', 'disabled');
CREATE TYPE NOTE_STYLE AS ENUM ('comment', 'markdown', 'file', 'target', 'grade');

CREATE TABLE users (
  "user_id" SERIAL PRIMARY KEY,
  "forename" TEXT NOT NULL,
  "surname" TEXT NOT NULL,
  "email_address" TEXT NOT NULL,
  "password_hash" TEXT NOT NULL,
  "account_type" ACCOUNT_TYPE NOT NULL,
  "account_status" STATUS DEFAULT 'enabled'
);
CREATE UNIQUE INDEX "email_address" ON users("email_address");

INSERT INTO users (forename, surname, email_address, password_hash, account_type)
VALUES ('Mike', 'Watts', 'mike@subdimension.co.uk', 'password', 'developer');

CREATE TABLE groups (
  "group_id" SERIAL PRIMARY KEY,
  "owner_id" INTEGER REFERENCES users("user_id") ON DELETE CASCADE,
  "group_name" TEXT
);
CREATE INDEX "groups_owner_id" ON groups("owner_id");

CREATE TABLE group_members (
  "group_id" INTEGER REFERENCES groups("group_id") ON DELETE CASCADE,
  "user_id" INTEGER REFERENCES users("user_id") ON DELETE CASCADE,
  PRIMARY KEY ("group_id", "user_id")
);

CREATE TABLE projects (
  "project_id" SERIAL PRIMARY KEY,
  "owner_id" INTEGER REFERENCES users("user_id") ON DELETE CASCADE,
  "title" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "date_created" TIMESTAMP DEFAULT current_timestamp,
  "deleted" BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX "project_owner" ON projects("owner_id");

CREATE TABLE project_members (
  "project_id" INTEGER REFERENCES projects("project_id") ON DELETE CASCADE,
  "user_id" INTEGER REFERENCES users("user_id") ON DELETE CASCADE,
  PRIMARY KEY ("project_id", "user_id")
);

CREATE TABLE notes (
  "note_id" SERIAL PRIMARY KEY,
  "project_id" INTEGER REFERENCES projects("project_id") ON DELETE CASCADE,
  "owner_id" INTEGER REFERENCES users("user_id") ON DELETE CASCADE,
  "content" TEXT, /* For files content = filename. URL is: {fileroot}/{owner_id}/{note_id}/{filename} */
  "style" NOTE_STYLE DEFAULT 'comment',
  "timestamp" TIMESTAMP DEFAULT current_timestamp
);
CREATE INDEX "note_owner" ON notes("owner_id");
CREATE INDEX "project_notes" ON notes("project_id");

CREATE TABLE note_links (
  "note_id" INTEGER REFERENCES notes("note_id") ON DELETE CASCADE,
  "links_to_note_id" INTEGER REFERENCES notes("note_id") ON DELETE CASCADE,
  PRIMARY KEY ("note_id", "links_to_note_id")
);
