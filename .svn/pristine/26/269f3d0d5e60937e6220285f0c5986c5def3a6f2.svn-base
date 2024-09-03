-- name: get-user-by-account^
-- record_class: UserInDB
SELECT id,
       account,
       phone,
       real_name,
       password,
       email,
       ifnull(witness_enable, 0) witness_enable,
       reg_time
FROM tb_user
WHERE account = :account;


-- name: get-user-by-phone^
-- record_class: UserInDB
SELECT id,
       account,
       phone,
       real_name,
       password,
       email,
       ifnull(witness_enable, 0) witness_enable,
       user_type,
       reg_time
FROM tb_user
WHERE phone = :phone;

-- name: get_userinfo_by_id^
-- record_class:UserInfoOutDB
select u.id, head_img, phone, real_name, ifnull(wechat_num, '') wechat_num, ifnull(address, '') address
from tb_user u
         left join tb_owner o on u.id = o.user_id
where u.id =:id;

-- name: get_witnessinfo_by_id^
-- record_class:WitnessInfoOutBD
select b.id,
       head_img,
       phone,
       real_name,
       ifnull(wechat_num, '') wechat_num,
       ifnull(b.address, '') address,
       site_code,
       ifnull(imgurl,'') site_img,
       order_enable
from (
         select u.id, head_img, phone, real_name, wechat_num, address, site_id,order_enable
         from tb_user u
                  left join tb_owner o on u.id = o.user_id) b
         left join tb_lottery_site s on b.site_id = s.id
where b.id = :id;

-- name: create-new-user<!
INSERT INTO tb_user (phone, account, password, witness_enable, user_status, user_type, reg_time)
VALUES (:phone, :account, :password, 0, 0, 1, now());


-- name: create_witness_user<!
insert into tb_witnesser_report (realname, phone_num, area, wechat_num, is_owner, imgurl, lottery_site_code, status,
                                 email, create_time, update_time)
values (:realname, :phone_num, :area, :wechat_num, :is_owner, :imgurl, :lottery_site_code, 0, '', now(), now());

-- name:get_witness_info_by_phone^
select id, phone_num
from tb_witnesser_report
where phone_num = :phone;

-- name:get_lottery_site_by_code^
select id, site_code
from tb_lottery_site
where site_code = :site_code;

-- name: get-owner-order-enable^
select order_enable from tb_owner where user_id= :userid