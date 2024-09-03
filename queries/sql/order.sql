-- name: get_order_list
-- record_class:OrderRecord
select *
from tb_order
where date_format(create_time, "%%Y-%%m-%%d") >= date_sub(curdate(), INTERVAL 7 DAY)
  and init_user_id = :userid
order by create_time;

-- name: get_no_order_count_by_owner
-- record_class:OrderCount
select lottery_center, a.cz_id, cz_name, count(*) total
from (
         select lottery_center, i.cz_id, cz_name, order_no
         from tb_order o
                  left join tb_cz_info i on o.cz_id = i.cz_id
         where REMIT_opt_id = :owner
           and REMIT_STATUS = 0) a
         right join (select distinct order_no from tb_tickets where Remit_limit_time > now()) t
                    on a.order_no = t.order_no
where a.order_no is not null
group by lottery_center, a.cz_id, cz_name;


-- name: get_order_by_cz_id
-- record_class: OrderRecord
select *
from tb_order
where cz_id = :cz_id
  and init_user_id = :userid
  and date_format(create_time, "%%Y-%%m-%%d") >= date_sub(curdate(), INTERVAL :dayval DAY)
order by create_time;

-- name: get_order_no_cp_by_cz_id^
-- record_class: OrderRecord
select id,
       a.order_no,
       cz_id,
       issue_name,
       order_num,
       order_money,
       init_user_id,
       active_id,
       pay_status,
       REMIT_STATUS,
       REMIT_time,
       ENCASH_STATUS,
       ENCASH_time,
       REMIT_content,
       ENCASH_pre_money,
       Remit_limit_time,
       create_time
from (
         select *
         from tb_order
         where cz_id = :cz_id
           and REMIT_STATUS = 0
           and REMIT_opt_id = :ownerid) a
         left join (select distinct order_no, Remit_limit_time from tb_tickets where Remit_limit_time > now()) t
                   on t.order_no = a.order_no
where Remit_limit_time is not null;

-- name: get_order_by_date
-- record_class:OrderRecord
select *
from tb_order
where date_format(create_time, "%%Y-%%m-%%d") >= date_sub(curdate(), INTERVAL :dayval DAY)
  and init_user_id = :userid
order by create_time;

-- name:create_order_by_active<!
insert into tb_order (order_no, init_user_id, cz_id, order_money, order_num, pay_status, issue_name, REMIT_STATUS,
                      create_time, active_id, ENCASH_STATUS)
values (:order_no, :user_id, :cz_id, :order_money, :order_num, 0, :issue_name, 0, now(), :active_id, 0);

-- name: create_order<!
insert into tb_order (order_no, init_user_id, cz_id, order_money, order_num, pay_status, issue_name, REMIT_STATUS,
                      create_time, ENCASH_STATUS)
values (:order_no, :user_id, :cz_id, :order_money, :order_num, 0, :issue_name, 0, now(), 0);

-- name: get_order_by_order_no^
-- record_class:OrderRecord
select *
from tb_order
where order_no = :order_no;

-- name: get_tickets_order_no
-- record_class:TicketRecord
select *
from tb_tickets
where order_no = :order_no;

-- name: set_tickets_jiedanid!
update tb_tickets
set REMIT_number= :REMIT_number
where id = :id;

-- name: get_ticket_list_by_order_no
-- record_class:TicketRecord
select *
from tb_tickets
where order_no in :order_no;


-- name: del_order_by_order_no<!
delete
from tb_order
where order_no = :order_no;

-- name: create_tickets_many*!
insert into tb_tickets (order_id, order_no, init_user_id, cz_id, wf_id, ticket_money, ticket_num, ticket_bs, content,
                        content_readable, create_time, issue_name)
values (:order_id, :order_no, :init_user_id, :cz_id, :wf_id, :ticket_money, :ticket_num, :ticket_bs, :content,
        :content_readable, now(), :issue_name);

-- name: create_ticket_one<!
insert into tb_tickets (order_id, order_no, init_user_id, cz_id, wf_id, ticket_money, ticket_num, ticket_bs, content,
                        content_readable, create_time,issue_name)
values (:order_id, :order_no, :init_user_id, :cz_id, :wf_id, :ticket_money, :ticket_num, :ticket_bs, :content,
        :content_readable, now(), :issue_name);

-- name: get_cz_info^
select *
from tb_cz_info
where cz_name = :czname
  and cz_id = :czid;

-- name: get_owner^
-- record_class: Owner
select *
from tb_owner
where user_id = :user_id;

# -- name: update_order_remit_status_by_order_no!
# update tb_order
# set REMIT_STATUS = 2,
#     REMIT_time=now()
# where order_no = :orderno
#   and REMIT_opt_id = :user_owner_id;

-- name: update_tickets_remit_status_by_order_no!
update tb_tickets
set REMIT_STATUS = 2,
    REMIT_time=now()
where order_no = :orderno
  and REMIT_opt_id = :user_owner_id;

-- name: update_order_img_remit_status_by_order_no
update tb_order
set REMIT_STATUS = 2,
    REMIT_time=now(),
    REMIT_content = :lottery_img
where order_no = :orderno
  and REMIT_opt_id = :user_owner_id;

-- name: serach_order_img_by_order_no^
select REMIT_STATUS, REMIT_content, ENCASH_STATUS, ENCASH_pre_money, ENCASH_time
from tb_order
where order_no = :order_no;

-- name: get_order_total
select count(tb_order.id), ifnull(sum(order_money), 0)
from tb_order
where pay_status = 1
  and REMIT_STATUS = 2
  and REMIT_opt_id = 22;

-- name: get_ticket_total
select i.cz_name, count(*) tickenum, sum(a.ticket_money) money
from (
         select o.order_no, tt.cz_id, o.pay_status, o.REMIT_STATUS, tt.ticket_money, o.REMIT_opt_id
         from tb_order o
                  left join tb_tickets tt on o.order_no = tt.order_no) a
         left join tb_cz_info i on a.cz_id = i.cz_id
where pay_status = 1
  and REMIT_STATUS = 2
  and REMIT_opt_id = 25
group by cz_name;

-- name: get_owner_order_list
-- record_class: Owner_Order_record
select id, cz_name, issue_name, ifnull(ENCASH_pre_money, 0) ENCASH_pre_money
from tb_order
         left join tb_cz_info tci on tb_order.cz_id = tci.cz_id
where pay_status = 1
  and REMIT_STATUS = 2
  and REMIT_opt_id = :ownerid;

-- name: get_owner_duijiang_record^
-- record_class: OrderRecord
select o.id,
       o.order_no,
       o.cz_id,
       o.issue_name,
       o.order_num,
       o.order_money,
       o.init_user_id,
       o.active_id,
       o.pay_status,
       o.REMIT_STATUS,
       o.ENCASH_pre_money,
       o.ENCASH_STATUS,
       o.REMIT_content,
       o.REMIT_time
from tb_order o
         right join (
    select * from tb_tickets where REMIT_number = :jiedanid and cz_id = :czid and issue_name = :qiciname) t
                    on o.order_no = t.order_no
where o.REMIT_opt_id = :userid;

-- name: get_order_money_by_orderid^
select order_money
from tb_order
where order_no = :orderNo;

-- name: update_order_pay_userid
update tb_order
set pay_opt_id= :userid
where order_no = :orderNo;

-- name: update_order_duijiang_status
update tb_order
set ENCASH_STATUS=2,
    ENCASH_pre_money= :prisemoney,
    ENCASH_time=now(),
    REMIT_content = :lottery_img
where order_no = :orderno;

-- name: update_tickets_duijiang_status
update tb_tickets
set ENCASH_STATUS=2,
    ENCASH_time=now()
where order_no = :orderno;

-- name: get_cz_info_list
select a.order_no,
       a.REMIT_time,
       a.issue_name,
       a.cz_id,
       a.order_money,
       a.REMIT_STATUS,
       a.ENCASH_STATUS,
       ifnull(a.ENCASH_pre_money, 0) ENCASH_pre_money,
       REMIT_number
from (
         select order_no,
                DATE_FORMAT(REMIT_time, "%%Y-%%m-%%d") REMIT_time,
                issue_name,
                cz_id,
                order_money,
                REMIT_STATUS,
                ENCASH_STATUS,
                ENCASH_pre_money
         from tb_order
         where REMIT_opt_id = :userid
           and REMIT_time between date_format(:sday, "%%Y-%%m-%%d") and date_format(:eday, "%%Y-%%m-%%d")
           and cz_id = (select cz_id from tb_cz_info where cz_name = :czname)) a
         left join tb_tickets t on a.order_no = t.order_no
where REMIT_number is not null;

-- name: get_owner_daystat_report
select date, remit_money, encash_money_prev
from tb_daystat_report
where owner_id = :ownerid
  and cz_id = 0
  and date between date_format(:sday, "%%Y-%%m-%%d") and date_format(:eday, "%%Y-%%m-%%d");

-- name: get_owner_daystat_report_type
select cz_name, remit_money, encash_money_prev
from tb_cz_info c
         right join (
    select cz_id, remit_money, encash_money_prev
    from tb_daystat_report
    where owner_id = :ownerid
      and cz_id != 0
      and date_format(date, "%%Y-%%m-%%d") = date_format(:days, "%%Y-%%m-%%d")) a on a.cz_id = c.cz_id;

-- name: stop_outer_ticket
update tb_owner
set order_enable = :state
where user_id = :userid