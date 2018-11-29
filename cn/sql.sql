/* 选择一个forum的所有文章 */
select
	article.id as article_id,
	article.time as article_time,
	article.title as article_title,
	article.abstract as article_abstract,
	article.content as article_content,
	article.source as article_source,
	article.source_link as article_source_link,
	article.title_bold as article_title_bold,
	forum.id as forum_id,
	forum.name as forum_name,
	catagory.id as catagory_id,
	catagory.name as catagory_name
from 
	forum inner join article on
		forum.id=article.forum_id 
	left join catagory on 
		article.catagory_id=catagory.id and catagory.forum_id=forum.id 
where
	forum.id=? order by article.id catagory.id desc 

QuickLinksCount=6
NewsForumId=2
/* 选择最新新闻 */
select * from forum inner join article on forum.id=article.forum_id where forum.id=NewsForumId order by article.id

RecommendArticlesForumId=12
/* 选择推荐文章 */
select * from article inner join quicklinks on article.id=quicklinks.article_id inner join forum on quicklinks.forum_id=forum.id where forum.id=RecommendArticlesForumId order by quicklinks.id desc limit 5

/* 选择一篇文章 */
select 
	article.id as article_id,
	article.time as article_time,
	article.title as article_title,
	article.abstract as article_abstract,
	article.content as article_content,
	article.source as article_source,
	article.source_link as article_source_link,
	article.title_bold as article_title_bold,
	forum.id as forum_id,
	forum.name as forum_name,
	catagory.id as catagory_id,
	catagory.name as catagory_name 
from
	article inner join forum on 
		forum.id=article.forum_id 
	left join catagory on 
		catagory.id=article.catagory_id and catagory.forum_id=forum.id 
where article.id=?

/* 插入一篇文章 */
insert into article (time,title,abstract,content,source,forum_id) values (?,?,?,?,?,?)
