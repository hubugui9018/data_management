-- name: get_video_by_id^
select count(id)
from tb_video
where id = :id;

-- name: get_video_js_by_id^
-- record_class: Video_Zan_Share
SELECT video_id, like_num, share_num
FROM tb_video_counter
WHERE video_id = :video_id;

-- name:update_video_zan
UPDATE tb_video_counter
set like_num = :like_num,
    last_like_time= now()
WHERE video_id = :video_id;

-- name:update_video_share
UPDATE tb_video_counter
set last_share_time = now(),
    share_num= :share_num
WHERE video_id = :video_id;

-- name:create_video_zan_share
insert into tb_video_counter (video_id, like_num, share_num, last_like_time,last_share_time)
VALUES (:video_id, :like_num, :share_num, now(),now());

-- name: get_videoinfo_by_id
-- record_class: Video
select a.id,
       a.title,
       video_url,
       like_num,
       share_num,
       a.head_img user_head_img,
       a.account  user_name,
       h.title    video_falg
from (
         select v.id,
                title,
                video_url,
                like_num,
                share_num,
                u.head_img,
                u.account,
                status
         from tb_video v
                  left join tb_user u on user_id = u.id) a
         right join tb_hot h on a.id = h.entity_id
where id = :id
  and status = 1;

-- name: get_video_max_id^
select max(id)
from tb_video
where status = 1;

-- name: get_video_list
-- record_class: Video
select b.id,
       b.title,
       b.video_url,
       b.video_falg,
       like_num,
       share_num,
       u.account,
       ifnull(u.head_img, "") user_head_img,
       u.account              user_name
from (select v.id, v.title, v.video_url, a.title video_falg, like_num, share_num, user_id
      from tb_video v
               right join (select * from tb_hot where title = :title) a on v.id = a.entity_id) b
         left join tb_user u on b.user_id = u.id;

