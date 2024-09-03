-- name: get_witness_content_by_activeid
-- record_class: WitnessContent
select active_id,
       real_name,
       head_img,
       text,
       imgurl,
       videourl,
       status,
       create_time
from tb_active_witness_info w
         left join tb_user u
                   on w.user_id = u.id
where active_id = :activeid
order by create_time desc;

-- name:create_witness_content<!
insert tb_active_witness_info (active_id, text, imgurl, videourl, user_id, status, create_time)
values (:active_id, :content, :imgurl, :videourl, :user_id, 0, now());

