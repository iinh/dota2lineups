create table if not exists lineups(
    lineup_key varchar(20) not null unique,
    wins integer not null default 0,
    losses integer not null default 0,
    win_rate real not null,
    weighted_sort real not null,
    primary key(lineup_key)
);

create table if not exists match_ids(
    lineup_key varchar(20) not null,
    match_id bigint not null,
    win boolean not null,
    primary key(lineup_key, match_id),
    foreign key(lineup_key) references lineups(lineup_key)
);

create table if not exists top_lineups(
    lineup_key varchar(20) not null unique,
    wins integer not null default 0,
    losses integer not null default 0,
    win_rate real not null,
    weighted_sort real not null,
    primary key(lineup_key),
    foreign key(lineup_key) references lineups(lineup_key)
);

create table if not exists info(
    last_update timestamp without time zone default (now() at time zone 'utc'),
    matches_parsed bigint
);
