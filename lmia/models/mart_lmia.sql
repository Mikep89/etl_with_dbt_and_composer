with clean_lmia as (
    select * from {{ ref('stg_lmia')}}
)

with lmia_by_province as (
    select province, sum(approved_lmias), sum(approved_positions)
    from clean_lmia
    group by province
)

with lmia_by_quarter as (
    select period, sum(approved_lmias), sum(approved_positions)
    from clean_lmia
    group by period
)

with lmia_by_company as (
    select company, sum(approved_lmias), sum(approved_positions)
    from clean_lmia
    group by company
)

select * from clean_lmia;
select * from lmia_by_company;
select * from lmia_by_province;
select * from lmia_by_quarter;