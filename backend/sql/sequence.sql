CREATE SEQUENCE "public"."user_pkey_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;



--建立自增user_pkey_seq
alter table user alter column id set default nextval('user_pkey_seq'); 

--设置字段开始自增的id
SELECT setval('user_pkey_seq', (SELECT MAX(id) FROM user)+1)

TRUNCATE  TABLE  user;//清空表数据
ALTER SEQUENCE user_pkey_seq RESTART WITH 1;//重置自增id从1开始