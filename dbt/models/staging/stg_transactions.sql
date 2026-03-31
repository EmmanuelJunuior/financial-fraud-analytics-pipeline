with raw as (
    select *
    from {{ ref('transactions_raw') }}
)

select
    step,
    type,
    amount,
    nameOrig,
    nameDest,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest,
    isFraud
from raw
