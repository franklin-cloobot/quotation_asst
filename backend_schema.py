#!/usr/bin/python

import psycopg2

conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")

print("Opened database successfully")
cur = conn.cursor()
cur.execute('''CREATE TABLE ORGANISATION
      (ORG_ID       TEXT     PRIMARY KEY,
      ORG_NAME      TEXT    NOT NULL,
      TIMESTAMP     INT     NOT NULL);
      ''')

cur.execute('''CREATE TABLE USERS
   (USER_ID               TEXT     NOT NULL,
    ORG_ID                TEXT     REFERENCES ORGANISATION(ORG_ID),
    USER_NAME             TEXT     NOT NULL,
    USER_PASSWORD         TEXT     NOT NULL,
    USER_PHONE            TEXT     NOT NULL,
    USER_EMAIL            TEXT     NOT NULL,
    AUTH_LEVEL            INT      NOT NULL,
    MANAGER_ID            TEXT     NOT NULL,
    TIMESTAMP             INT      NOT NULL,
    product_constraints   TEXT     NOT NULL,
    location_constraints  TEXT     NOT NULL);
    ''')

cur.execute('''CREATE TABLE CLIENT
      (C_ID                     TEXT                     NOT NULL,
      ORG_ID                    TEXT                     REFERENCES ORGANISATION(ORG_ID),
      C_NAME                    TEXT                    NOT NULL,
      C_PHONE                   TEXT                    NOT NULL,
      C_MAIL                    TEXT                    NOT NULL,
      C_ADDRESS                 TEXT                    NOT NULL,
      TIMESTAMP                 INT                     NOT NULL);
      ''')

cur.execute('''CREATE TABLE PRODUCT
      (P_ID                 TEXT                     NOT NULL,
      ORG_ID                TEXT                     REFERENCES ORGANISATION(ORG_ID),
      P_DESC                TEXT                    NOT NULL,
      P_CATEGORY            TEXT                    NOT NULL,
      P_CODE                TEXT                    NOT NULL,
      TIMESTAMP             INT                     NOT NULL);
      ''')

cur.execute('''CREATE TABLE QUOTES
      (Q_ID                 TEXT                     NOT NULL,
      ORG_ID                TEXT                     REFERENCES ORGANISATION(ORG_ID),
      USER_ID               TEXT                     NOT NULL,
      C_ID                  TEXT                     NOT NULL,
      P_ID                  TEXT                     NOT NULL,
      QTY                   INT                      NOT NULL,
      UNIT_PRICE            INT                      NOT NULL,
      SALES_EXEC_ID         TEXT                     NOT NULL,
      SALES_MANAGER_ID      TEXT                     NOT NULL,
      CHAT_CONVERSATION     TEXT                     NOT NULL,
      EMAIL_CONVERSATION    TEXT                     NOT NULL,
      TIMESTAMP             INT                      NOT NULL,
      thread_id             TEXT                     NOT NULL,
      SESSION_ID            INT                      NOT NULL);
      ''')

cur.execute('''CREATE TABLE TEMP
      (TEMP_ID SERIAL,
      U_ID       TEXT    NOT NULL,
      COMMAND    TEXT    NOT NULL,
      STATUS     TEXT    NOT  NULL,
      TIMESTAMP  INT     NOT NULL,
      n_th_input INT,
      session_id INT,
      dealer     TEXT,
      options    TEXT,
      product    TEXT,
      price      TEXT,
      quantity   TEXT);
      ''')

cur.execute('''CREATE TABLE SESSION
      (
      SESSION_ID        SERIAL,
      U_ID              TEXT    NOT NULL,
      CONVERSATION      TEXT    NOT NULL,
      TIMESTAMP         INT     NOT NULL,
      DEALER            TEXT,
      current_option    INT);
      ''')


conn.commit()
conn.close()