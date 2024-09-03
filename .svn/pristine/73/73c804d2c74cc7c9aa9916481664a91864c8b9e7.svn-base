-- name: get_actvie_by_type_of_rot
-- record_class: Active
select i.id,
       i.province,
       act_title,
       begin_date,
       end_date,
       ifnull(begin_issue, "") as           begin_issue,
       prize_type,
       IFNULL(city, '')                     city,
       ifnull(end_issue, "")   as           end_issue,
       lottery_cz,
       i.lottery_type,
       active_type,
       ifnull(i.forward_num, 0)             forward_num,
       ifnull(i.like_num, 0)                like_num,
       ifnull(i.support, 0)             support,
       ifnull(i.nosupport, 0)                nosupport,
       ifnull(i.witness_num, 0)             witness_num,
       ifnull(cz_logo_url, '')              lottimgurl,
       ifnull(imgurl, '')                   imgurl,
       ifnull(videourl, '')                 videourl,
       ifnull(`desc`, '')                   active_disc,
       concat(i.province, i.lottery_center) lcenter,
       degree
from (
         select active_id, degree, status
         from tb_active_categorize
         where begin_time is not NULL
           and datediff(begin_time, curdate()) <= 0
           and (end_time is null or datediff(end_time, curdate()) >= 0)
           and (duration = 0 or date_add(begin_time, INTERVAL duration day) >= curdate())) c
         left join (
    select c.id,
           c.province,
           act_title,
           begin_date,
           end_date,
           begin_issue,
           prize_type,
           end_issue,
           lottery_cz,
           lottery_type,
           active_type,
           forward_num,
           like_num,
           support,
           nosupport,
           cz_logo_url,
           witness_num,
           imgurl,
           videourl,
           `desc`,
           city,
           c.lottery_center
    from (
             select a.id,
                    zixun_id,
                    a.province,
                    prize_type,
                    act_title,
                    a.lottery_center,
                    begin_date,
                    end_date,
                    begin_issue,
                    cz_logo_url,
                    city,
                    end_issue,
                    lottery_cz,
                    lottery_type,
                    active_money,
                    active_type,
                    b.forward_num,
                    b.like_num,
                    b.support,
                    b.nosupport,
                    `desc`,
                    imgurl,
                    videourl
             from (
                      select ai.id,
                             zixun_id,
                             o.province,
                             prize_type,
                             act_title,
                             o.lottery_center,
                             begin_date,
                             end_date,
                             begin_issue,
                             cz_logo_url,
                             city,
                             end_issue,
                             lottery_cz,
                             lottery_type,
                             active_money,
                             active_type,
                             `desc`,
                             img_url   imgurl,
                             video_url videourl
                      from tb_active_info ai
                               left join tb_organization o on ai.organization_id = o.id) a
                      left join tb_active_counter b on a.id = b.active_id) c
             left join (
        select active_id, count(active_id) witness_num from tb_active_witness_info group by active_id) f
                       on c.id = f.active_id) i on c.active_id = i.id
WHERE (timestampdiff(SECOND ,now(),end_date) > 0 or end_date is null)
  and status = 1
order by degree desc, begin_date desc;

-- name: get_actvie_by_province
-- record_class: Active
select c.id,
       c.province,
       act_title,
       begin_date,
       end_date,
       ifnull(begin_issue, "") as           begin_issue,
       prize_type,
       IFNULL(city, '')                     city,
       ifnull(end_issue, "")   as           end_issue,
       lottery_cz,
       c.lottery_type,
       active_type,
       ifnull(c.forward_num, 0)             forward_num,
       ifnull(c.like_num, 0)                like_num,
       ifnull(c.support, 0)             support,
       ifnull(c.nosupport, 0)                nosupport,
       ifnull(g.witness_num, 0)             witness_num,
       ifnull(cz_logo_url, '')              lottimgurl,
       ifnull(imgurl, '')                   imgurl,
       ifnull(videourl, '')                 videourl,
       ifnull(`desc`, '')                   active_disc,
       concat(c.province, c.lottery_center) lcenter
from (
         select a.id,
                zixun_id,
                a.province,
                prize_type,
                act_title,
                a.lottery_center,
                begin_date,
                end_date,
                begin_issue,
                cz_logo_url,
                city,
                end_issue,
                lottery_cz,
                lottery_type,
                active_money,
                active_type,
                b.forward_num,
                b.like_num,
                b.support,
                b.nosupport,
                `desc`,
                imgurl,
                videourl
         from (
                  select ai.id,
                         zixun_id,
                         o.province,
                         prize_type,
                         act_title,
                         o.lottery_center,
                         begin_date,
                         end_date,
                         begin_issue,
                         cz_logo_url,
                         city,
                         end_issue,
                         lottery_cz,
                         lottery_type,
                         active_money,
                         active_type,
                         `desc`,
                         img_url   imgurl,
                         video_url videourl
                  from tb_active_info ai
                           left join tb_organization o on ai.organization_id = o.id) a
                  left join tb_active_counter b on a.id = b.active_id) c
         left join (
    select active_id, count(active_id) witness_num from tb_active_witness_info group by active_id) g
                   on c.id = g.active_id
WHERE (timestampdiff(SECOND ,now(),end_date) > 0 or end_date is null)
and province = :province
order by begin_date desc;

-- name: get_actvie_by_type_of_paijiang
-- record_class: Active
select c.id,
       c.province,
       act_title,
       begin_date,
       end_date,
       ifnull(begin_issue, "") as           begin_issue,
       prize_type,
       IFNULL(city, '')                     city,
       ifnull(end_issue, "")   as           end_issue,
       lottery_cz,
       c.lottery_type,
       active_type,
       ifnull(c.forward_num, 0)             forward_num,
       ifnull(c.like_num, 0)                like_num,
       ifnull(c.support, 0)             support,
       ifnull(c.nosupport, 0)                nosupport,
       ifnull(f.witness_num, 0)             witness_num,
       ifnull(cz_logo_url, '')              lottimgurl,
       ifnull(imgurl, '')                   imgurl,
       ifnull(videourl, '')                 videourl,
       ifnull(`desc`, '')                   active_disc,
       concat(c.province, c.lottery_center) lcenter
from (
         select a.id,
                zixun_id,
                a.province,
                prize_type,
                act_title,
                a.lottery_center,
                begin_date,
                end_date,
                begin_issue,
                cz_logo_url,
                city,
                end_issue,
                lottery_cz,
                lottery_type,
                active_money,
                active_type,
                b.forward_num,
                b.like_num,
                b.support,
                b.nosupport,
                `desc`,
                imgurl,
                videourl
         from (
                  select ai.id,
                         zixun_id,
                         o.province,
                         prize_type,
                         act_title,
                         o.lottery_center,
                         begin_date,
                         end_date,
                         begin_issue,
                         cz_logo_url,
                         city,
                         end_issue,
                         lottery_cz,
                         lottery_type,
                         active_money,
                         active_type,
                         `desc`,
                         img_url   imgurl,
                         video_url videourl
                  from tb_active_info ai
                           left join tb_organization o on ai.organization_id = o.id) a
                  left join tb_active_counter b on a.id = b.active_id) c
         left join (
    select active_id, count(active_id) witness_num from tb_active_witness_info group by active_id) f
                   on c.id = f.active_id
WHERE active_type = 2
  and (timestampdiff(SECOND ,now(),end_date) > 0 or end_date is null)
  order by begin_date desc;


-- name: get_actvie_by_type_of_wupin
-- record_class: Active
select g.id,
       g.province,
       act_title,
       begin_date,
       end_date,
       ifnull(begin_issue, "") as           begin_issue,
       prize_type,
       IFNULL(city, '')                     city,
       ifnull(end_issue, "")   as           end_issue,
       lottery_cz,
       g.lottery_type,
       active_type,
       ifnull(g.forward_num, 0)             forward_num,
       ifnull(g.like_num, 0)                like_num,
       ifnull(g.support, 0)             support,
       ifnull(g.nosupport, 0)                nosupport,
       ifnull(g.witness_num, 0)             witness_num,
       ifnull(cz_logo_url, '')              lottimgurl,
       ifnull(imgurl, '')                   imgurl,
       ifnull(videourl, '')                 videourl,
       ifnull(`desc`, '')                   active_disc,
       concat(g.province, g.lottery_center) lcenter
from (
         select c.id,
                c.province,
                act_title,
                begin_date,
                end_date,
                begin_issue,
                prize_type,
                end_issue,
                lottery_cz,
                lottery_type,
                active_type,
                forward_num,
                support,
                nosupport,
                like_num,
                cz_logo_url,
                witness_num,
                imgurl,
                videourl,
                `desc`,
                city,
                c.lottery_center
         from (select a.id,
                      zixun_id,
                      a.province,
                      prize_type,
                      act_title,
                      a.lottery_center,
                      begin_date,
                      end_date,
                      begin_issue,
                      cz_logo_url,
                      city,
                      end_issue,
                      lottery_cz,
                      lottery_type,
                      active_money,
                      active_type,
                      b.forward_num,
                      b.like_num,
                      b.nosupport,
                      b.support,
                      `desc`,
                      imgurl,
                      videourl
               from (
                        select ai.id,
                               zixun_id,
                               o.province,
                               prize_type,
                               act_title,
                               o.lottery_center,
                               begin_date,
                               end_date,
                               begin_issue,
                               cz_logo_url,
                               city,
                               end_issue,
                               lottery_cz,
                               lottery_type,
                               active_money,
                               active_type,
                               `desc`,
                               img_url   imgurl,
                               video_url videourl
                        from tb_active_info ai
                                 left join tb_organization o on ai.organization_id = o.id) a
                        left join tb_active_counter b on a.id = b.active_id) c
                  left join (
             select active_id, count(active_id) witness_num from tb_active_witness_info group by active_id) f
                            on c.id = f.active_id) g
         right join (select distinct active_id from tb_active_award_type where type_name = :type_name) t
                    on g.id = t.active_id
where timestampdiff(SECOND ,now(),end_date) > 0
   or end_date is null
   order by begin_date desc;

-- name: get_active_count_data^
-- record_class: ActiveCount
select sum(case  when datediff(create_time,now())=0 then 1 else 0 end ) new,
       sum(case  when datediff(begin_date,now())=0 then 1 else 0 end ) will ,
       sum(case  when end_date>curdate() or (end_date is null and begin_date<now()) then 1 else 0 end ) total
from tb_active_info;

-- name: get_active_count_data_by_province^
-- record_class: ActiveCount
select sum(case  when datediff(create_time,now())=0 then 1 else 0 end ) new,
       sum(case  when datediff(begin_date,now())=0 then 1 else 0 end ) will ,
       sum(case  when end_date>curdate() or (end_date is null and begin_date<now()) then 1 else 0 end ) total
from tb_active_info
where province like :province;

-- name: get_active_count_data_by_provinces
-- record_class: ActiveCountProvince
select province, sum(case when datediff(create_time, now()) = 0 then 1 else 0 end)  new,
       sum(case when datediff(begin_date, now()) = 0 then 1 else 0 end) will,
       sum(case when end_date > curdate() or (end_date is null and begin_date < now()) then 1 else 0 end) total
from tb_active_info group by province;

-- name: get_active_by_id^
-- record_class: Active
select g.id,
       g.province,
       act_title,
       begin_date,
       end_date,
       ifnull(begin_issue, "") as           begin_issue,
       prize_type,
       IFNULL(city, '')                     city,
       ifnull(end_issue, "")   as           end_issue,
       lottery_cz,
       g.lottery_type,
       active_type,
       ifnull(g.forward_num, 0)             forward_num,
       ifnull(g.like_num, 0)                like_num,
       ifnull(g.support, 0)             support,
       ifnull(g.nosupport, 0)                nosupport,
       ifnull(g.witness_num, 0)             witness_num,
       ifnull(cz_logo_url, '')              lottimgurl,
       ifnull(imgurl, '')                   imgurl,
       ifnull(videourl, '')                 videourl,
       ifnull(`desc`, '')                   active_disc,
       concat(g.province, g.lottery_center) lcenter
from (
         select c.id,
                c.province,
                act_title,
                begin_date,
                end_date,
                begin_issue,
                prize_type,
                end_issue,
                lottery_cz,
                lottery_type,
                active_type,
                forward_num,
                nosupport,
                support,
                like_num,
                cz_logo_url,
                witness_num,
                imgurl,
                videourl,
                `desc`,
                city,
                c.lottery_center
         from (
                  select a.id,
                         zixun_id,
                         a.province,
                         prize_type,
                         act_title,
                         a.lottery_center,
                         begin_date,
                         end_date,
                         begin_issue,
                         cz_logo_url,
                         city,
                         end_issue,
                         lottery_cz,
                         lottery_type,
                         active_money,
                         active_type,
                         b.forward_num,
                         b.like_num,
                         b.nosupport,
                         b.support,
                         `desc`,
                         imgurl,
                         videourl
                  from (
                           select ai.id,
                                  zixun_id,
                                  o.province,
                                  prize_type,
                                  act_title,
                                  o.lottery_center,
                                  begin_date,
                                  end_date,
                                  begin_issue,
                                  cz_logo_url,
                                  city,
                                  end_issue,
                                  lottery_cz,
                                  lottery_type,
                                  active_money,
                                  active_type,
                                  `desc`,
                                  img_url   imgurl,
                                  video_url videourl
                           from tb_active_info ai
                                    left join tb_organization o on ai.organization_id = o.id) a
                           left join tb_active_counter b on a.id = b.active_id) c
                  left join (
             select active_id, count(active_id) witness_num from tb_active_witness_info group by active_id) f
                            on c.id = f.active_id) g
         left join tb_cz_info i on g.lottery_cz = i.cz_name
where id = :id;


-- name: get_active_supple_by_id
-- record_class: Active_Supplementary
select itemname,item_content
from tb_active_supplementary
where active_id=:id and itemname not in ('imgurl','videourl') order by id asc;

-- name: get_active_article_by_id
SELECT about_id,about_title,about_url
FROM tb_active_about
WHERE active_id = :id;

-- name: get_active_relate
SELECT id,prize_type,act_title
FROM tb_active_info
where lottery_cz = :lotteryname and datediff(begin_date,curdate())<0 and (datediff(end_date,curdate())>0 or end_date is null);

-- name:get_active_js_by_id^
-- record_class:Active_Zan_Share
SELECT active_id,like_num,forward_num,support,nosupport
FROM tb_active_counter
WHERE active_id = :active_id;

-- name:update_active_zan_share
UPDATE tb_active_counter
set like_num = :like_num, forward_num= :forward_num,support= :support,nosupport= :nosupport
WHERE active_id = :active_id;


-- name:create_active_zan_share
insert into tb_active_counter (active_id,like_num,forward_num,support,nosupport)
values (:active_id, :like_num, :forward_num, :support, :nosupport);

-- name:get_actvie_item_by_id
-- record_class:Active_Item
select  platform_name platfrom,enter_url,activity_rule act_rule
from tb_active_item_info
where active_id=:act_id;

-- name:get_wx_operating^
-- record_class:Active_Ask
select name, phone, wx_name, wx_img
from tb_wx_operating
where state = 1

-- name:get_active_by_tuijian
-- record_class:BaseActive
select a.id,lottery_type,
       lottery_cz,
       ifnull(cz_logo_url, '') lottimgurl,
       act_title,
       province,
       prize_type
from tb_active_info a
         right join (
    select * from tb_active_categorize where status = 1 order by degree desc, begin_time desc limit 5) b on
    a.id = b.active_id;

-- name:check_active_is_exists_by_id
select id from tb_active_info where id=:id;