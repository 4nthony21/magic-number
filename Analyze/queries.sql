SELECT rev.description,
    sum(revenue) revenue,
    round(avg(rev.revenue*100/rev.sales),2) margin
FROM
(
    select
        a.description,
        sum(a.salesprice) sales,
        sum(b.PurchasePrice) purchase,
        sum(a.salesprice - (b.PurchasePrice)) revenue
    
    from salesdec a
    left join pricingpurchasesdec b
    on a.Brand = b.Brand
    where b.PurchasePrice <> 0
    group by a.description
) rev
GROUP BY rev.description