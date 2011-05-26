insert into mg_user (mailbox) values ('silegon@gmail.com'),('zoom.quiet@gmail.com'),('zsp007@gmail.com');

insert into mg_group (gname) values ('42qu'),('cpyug'),('woodpecker');

insert into user_group (group_id, user_id, status) values (1,1,1),(2,1,99),(3,1,1),(2,2,1),(3,2,99),(1,3,99),(2,3,1);

select mg_user.mailbox, mg_group.gname, user_group.status from mg_user,user_group,mg_group where mg_user.id = user_group.user_id and mg_group.id=user_group.group_id ;

select mg_user.mailbox, mg_group.gname, user_group.status from mg_user,user_group,mg_group where mg_user.id = user_group.user_id and mg_group.id=user_group.group_id and mg_user.mailbox="silegon@gmail.com" and mg_group.gname="cpyug";



