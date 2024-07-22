# Tags
- Android
- Messages

# Intro

Cyber Police have seized a computer containing illegal content, but the data stored is secured with a password.

A member of the criminal organization owning the computer was arrested. Police suspect that the password was sent to the criminal via SMS, but the message was deleted right before the arrest.

You’re given a dump of the data partition of the phone (running Android 6.0). Your job as the forensic specialist is to recover the deleted password.

# Solution

Extracting the tar given: `tar -xvzf data.tar.gz ` we get a dump of a android OS.
Our goal is to recover the content of deleted SMSs.

Android stores the messages(https://www.magnetforensics.com/blog/android-messaging-forensics-sms-mms-and-beyond/) in the following database: `/data/data/com.android.providers.telephony/databases/mmssms.db`. 
In some versions we can have it in: `/data/user/0/com.android.providers.telephony/databases/mmssms.db`. 
Lets look for it: `find ./data -name "*mmssms*"`

```
./data/data/com.google.android.gms/databases/icing_mmssms.db
./data/data/com.google.android.gms/databases/icing_mmssms.db-journal
./data/data/com.google.android.gms/databases/ipa_mmssms.db
./data/data/com.google.android.gms/databases/ipa_mmssms.db-journal
./data/data/com.android.providers.telephony/databases/mmssms.db
./data/data/com.android.providers.telephony/databases/mmssms.db-journal
./data/user/0/com.google.android.gms/databases/icing_mmssms.db
./data/user/0/com.google.android.gms/databases/icing_mmssms.db-journal
./data/user/0/com.google.android.gms/databases/ipa_mmssms.db
./data/user/0/com.google.android.gms/databases/ipa_mmssms.db-journal
./data/user/0/com.android.providers.telephony/databases/mmssms.db
./data/user/0/com.android.providers.telephony/databases/mmssms.db-journal
```

Using the tool(https://sqlitebrowser.org/dl/) to open the .db files, we found nothing in the SMS tables. 
Looking at the previous mentioned article() we keep looking for each database mentioned and can't find nothing.
However the "Android messages" app is not storing the conversations in the path given by the article. It is in(https://www.reddit.com/r/LineageOS/comments/p8fx6e/where_are_text_messages_stored/): `/data/user/0/com.android.messaging/databases/bugle_db`. As explained in the article this database stores the "Android Messages" which is a message app that some carriers install by default.
Looking at the tables of this database we found a table called parts which contains the flag: `uctf{l057_1n_urm14}`