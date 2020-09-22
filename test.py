import requests

req = requests.post("http://127.0.0.1:8001/register")
print(req.text)

 select q.q_id,(select c_name from client where c_id = q.c_id),(select p_code from product where p_id = q.p_id),(select p_desc from product where p_id = q.p_id),qty,unit_price,sales_exec_id,(select user_name from users where user_id = q.user_id),(qty * unit_price) total,(select product_constraints from users where user_id = q.user_id) from quotes q where p_id in (select p_id from product where lower(p_code) like (select product_constraints from users where user_id = q.user_id));