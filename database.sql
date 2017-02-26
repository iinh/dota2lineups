set FOREIGN_KEY_CHECKS = 0;
drop table if exists lineups ;
set FOREIGN_KEY_CHECKS = 1;

create table lineups(
        lineup_key varchar(20) not null unique,
        wins integer not null default 0,
        losses integer not null default 0,
        win_rate double not null,
        primary key(lineup_key)
        );

create table match_ids(
    lineup_key varchar(20) not null,
    match_id integer not null,
    primary key(lineup_key, match_id)
    foreign key(lineup_key) references lineups(lineup_key)
);
