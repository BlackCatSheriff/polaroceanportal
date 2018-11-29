create table if not exists board (
					id integer primary key,
					name text not null
					);
					
create table if not exists catagory (
					id integer primary key,
					name text not null,
					board_id integer not null references board(id)
						on update cascade
						on delete restrict
					);

create table if not exists article (
					id integer primary key,
					time text not null,
					title text not null,
					abstract text,
					content text,
					source text,
					source_link text,
					title_bold integer default 0,
					board_id integer not null references board(id)
						on update cascade
						on delete restrict,
					
					catagory_id integer references catagory(id)
						on update cascade
						on delete restrict
);

create table if not exists quicklinks (
					id integer primary key,
					board_id integer not null references board(id)
						on update cascade
						on delete restrict,
					article_id integer not null unique references article(id)
						on update cascade
						on delete cascade
);
					
create table if not exists users (
					id integer primary key,
					name text not null unique,
					passwd text not null
);

create table if not exists setting(
					id integer primary key,
					key integer not null,
					name text not null,
					value text,
					parent_id integer references setting(id)
						on update cascade
						on delete cascade
);
					

