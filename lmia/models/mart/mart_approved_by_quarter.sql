{{ config(materialized= "view")}}
select period as period, 
sum(approved_lmias) as approved_lmias, 
sum(approved_positions) as approved_positions
from {{ ref('stg_lmia') }}
group by period