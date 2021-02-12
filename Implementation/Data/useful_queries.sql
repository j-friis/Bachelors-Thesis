select count_, count(*) as counts from _775147 group by count_ ORDER BY counts DESC;
select count(DISTINCT  count_) from _775147;
select count(*) as number_of_dates, count(DISTINCT  count_) as distinct_count from _775147;

[jfriis]~>$ sudo su - postgres
postgres@jfriis:~$ createdb bachelorBesoeg2014


