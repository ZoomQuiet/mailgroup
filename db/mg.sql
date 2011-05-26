use mailgroup;
create table mg_user(
    id int primary key auto_increment not null,
    signature   varchar(200),
    mailbox     varchar(45)
)default charset=utf8 ;
alter table mg_user add unique index mailbox_idx(mailbox);

create table mg_group(
    id int primary key auto_increment not null,
    gname varchar(20) not null
)default charset=utf8;
alter table mg_group add unique index gname_idx(gname);

create table user_group(
    group_id int not null,
    user_id int not null,
    status int default 1
)default charset=utf8;
alter table user_group add primary key (group_id, user_id);

create table topic(
    id int primary key auto_increment not null,
    topic varchar(100),
    topic_desc varchar(255),
    mailgroup_id int not null
)default charset=utf8;

create table mail(
    id int primary key auto_increment not null,
    topic_id int not null,
    message_id varchar(100),
    body text,
    create_time datetime,
    sender_mailbox  varchar(45),
    mailgroup int,
    status int
)default charset=utf8;
alter table mail add index topic_id_idx(topic_id);
alter table mail add unique index message_id_idx(message_id);
