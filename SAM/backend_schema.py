#!/usr/bin/python

import psycopg2

# conn = psycopg2.connect(database="allotment", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")
conn = psycopg2.connect(database="allotment", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
print("Opened database successfully")
cur = conn.cursor()

cur.execute('''CREATE TABLE USERS
   (USER_ID               SERIAL,
    USER_NAME             TEXT     NOT NULL,
    USER_PASSWORD         TEXT     NOT NULL,
    USER_PHONE            TEXT     NOT NULL,
    USER_EMAIL            TEXT     NOT NULL,
    USER_AUTH_LEVEL       INT      NOT NULL,
    USER_ROLE             TEXT     NOT NULL,
    USER_TL               TEXT     NOT NULL,
    USER_PROJ_TYPE        TEXT     NOT NULL,
    TIMESTAMP             INT      NOT NULL);
    ''')

cur.execute('''CREATE TABLE customer
   (cust_ID               SERIAL,
    cust_NAME             TEXT     NOT NULL,
    cust_PASSWORD         TEXT     NOT NULL,
    cust_PHONE            TEXT     NOT NULL,
    cust_EMAIL            TEXT     NOT NULL,
    TIMESTAMP             INT      NOT NULL);
    ''')

cur.execute('''CREATE TABLE PROJECT
      (P_ID                         SERIAL,
      P_NAME                        TEXT                    NOT NULL,
      P_DETAIL                      TEXT                    NOT NULL,
      P_DOCS                        TEXT                    NOT NULL,
      P_MANUAL_OVERRIDE             TEXT                    NOT NULL,
      P_TYPE                        TEXT                    NOT NULL,
      P_TL                          TEXT                    NOT NULL,
      P_CHECK                       INT                     NOT NULL,
      P_ESTIMATE                    INT                     NOT NULL,
      P_CE                          TEXT                    NOT NULL,
      P_ALOT_TIME                   INT                     NOT NULL,
      P_DONE_TIME                   INT                     NOT NULL,
      P_LAST_REM                    INT                     NOT NULL,
      P_TOTAL_REM                   INT                     NOT NULL,
      P_STATUS                      INT                     NOT NULL);
      ''')





conn.commit()
conn.close()