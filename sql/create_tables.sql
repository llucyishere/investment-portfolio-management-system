
create database if not exists investment_portfolio;

use investment_portfolio;

create table MEMBER (
    member_id int primary key auto_increment,
    name varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null,
    birth_date date not null
);

create table STOCK (
    stock_code varchar(6) primary key,
    stock_name varchar(255) not null unique
);

create table TRANSACTION_HISTORY(
    transaction_id int primary key auto_increment,
    member_id int not null,
    stock_code varchar(6) not null,
    transaction_date date not null,
    transaction_type varchar(10) not null,
    quantity int not null,
    price int not null,
    foreign key (member_id) references MEMBER(member_id),
    foreign key (stock_code) references STOCK(stock_code)
);

create table WATCHLIST(
    watchlist_id int primary key auto_increment,
    member_id int not null,
    stock_code varchar(6) not null,
    foreign key (member_id) references MEMBER(member_id),
    foreign key (stock_code) references STOCK(stock_code),
    unique(member_id, stock_code)
);  