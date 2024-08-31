WITH customer_spending AS (
    SELECT
        o.customer_id,
        c.customer_name,
        c.email,
        SUM(oi.quantity * oi.price_per_unit) AS total_spent
    FROM
        Orders o
    JOIN
        Customers c ON o.customer_id = c.customer_id
    JOIN
        Order_Items oi ON o.order_id = oi.order_id
    WHERE
        o.order_date >= DATE('now', '-1 year')
    GROUP BY
        o.customer_id
),
category_spending AS (
    SELECT
        o.customer_id,
        p.category,
        SUM(oi.quantity * oi.price_per_unit) AS category_spent
    FROM
        Orders o
    JOIN
        Order_Items oi ON o.order_id = oi.order_id
    JOIN
        Products p ON oi.product_id = p.product_id
    WHERE
        o.order_date >= DATE('now', '-1 year')
    GROUP BY
        o.customer_id, p.category
),
ranked_categories AS (
    SELECT
        cs.customer_id,
        cs.category,
        cs.category_spent,
        RANK() OVER (PARTITION BY cs.customer_id ORDER BY cs.category_spent DESC) AS rank
    FROM
        category_spending cs
)
SELECT
    cs.customer_id,
    c.customer_name,
    c.email,
    cs2.total_spent,
    cs.category AS most_purchased_category
FROM
    ranked_categories cs
JOIN customer_spending cs2 ON cs.customer_id = cs2.customer_id
JOIN Customers c ON cs.customer_id = c.customer_id
WHERE
    cs.rank = 1
ORDER BY
    cs2.total_spent DESC
LIMIT 5;
