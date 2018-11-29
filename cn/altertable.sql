create table if not exists new_article (
					id integer primary key,
					time text not null,
					title text not null,
					abstract text,
					content text,
					source text,
					stick_index integer,
					title_bold integer default 0,
					board_id integer not null references board(id)
						on update cascade
						on delete restrict,
					
					catagory_id integer references catagory(id)
						on update cascade
						on delete restrict
);

insert into new_article (id,time,title,abstract,content,source,title_bold,board_id,catagory_id) select id,time,title,abstract,content,source,title_bold,board_id,catagory_id from article;

drop table article;

alter table new_article rename to article;
