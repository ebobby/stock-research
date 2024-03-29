DROP VIEW IF EXISTS stock_dcf_analysis;
DROP VIEW IF EXISTS stock_simple_analysis;
DROP VIEW IF EXISTS stock_buffettology_report;
DROP MATERIALIZED VIEW IF EXISTS stock_5y_averages;
DROP MATERIALIZED VIEW IF EXISTS stock_5y_report;
DROP MATERIALIZED VIEW IF EXISTS stock_general_report_with_growth;
DROP MATERIALIZED VIEW IF EXISTS stock_general_report;
DROP AGGREGATE median(anyelement);
DROP FUNCTION growth;
DROP FUNCTION to_millions;
DROP FUNCTION cagr;
DROP FUNCTION _final_median;

-- From https://wiki.postgresql.org/wiki/Aggregate_Median
CREATE OR REPLACE FUNCTION _final_median(anyarray) RETURNS decimal AS $$
  WITH q AS
  (
     SELECT val
     FROM unnest($1) val
     WHERE VAL IS NOT NULL
     ORDER BY 1
  ),
  cnt AS
  (
    SELECT COUNT(*) as c FROM q
  )
  SELECT AVG(val)::decimal
  FROM
  (
    SELECT val FROM q
    LIMIT  2 - MOD((SELECT c FROM cnt), 2)
    OFFSET GREATEST(CEIL((SELECT c FROM cnt) / 2.0) - 1,0)
  ) q2;
$$ LANGUAGE sql IMMUTABLE;

CREATE OR REPLACE AGGREGATE median(anyelement) (
  SFUNC=array_append,
  STYPE=anyarray,
  FINALFUNC=_final_median,
  INITCOND='{}'
);

CREATE OR REPLACE FUNCTION growth(after DECIMAL, before DECIMAL) RETURNS DECIMAL AS $$
BEGIN
  RETURN CASE
    WHEN before <> 0 THEN ROUND((after - before) / ABS(before), 3)
    ELSE 0 END;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION to_millions(amount DECIMAL) RETURNS DECIMAL AS $$
BEGIN
  RETURN ROUND(amount/1000000,2);
END;
$$ LANGUAGE plpgsql;

-- compound annual growth rate
CREATE OR REPLACE FUNCTION cagr(ending DECIMAL, beginning DECIMAL, years DECIMAL) RETURNS DECIMAL AS $$
BEGIN
  RETURN CASE
    WHEN beginning = 0 THEN 'NAN'::decimal
    WHEN ending = 0 THEN 0
    WHEN ending < 0 THEN -1
    WHEN beginning < 0 THEN 'NAN'::decimal
    ELSE ROUND(POWER(ending / beginning, 1::decimal / years) - 1, 3) END;
END;
$$ LANGUAGE plpgsql;

DROP MATERIALIZED VIEW IF EXISTS stock_general_report;
CREATE MATERIALIZED VIEW stock_general_report AS
(
    SELECT DISTINCT
      stocks.id stock_id,
      stocks.symbol,
      income_statements.report_date AS date,
      income_statements.report_type AS type,
      RANK() OVER (PARTITION BY stocks.symbol, income_statements.report_type ORDER BY income_statements.report_date DESC) AS report_number,
      --------------------------------------------------
      -- General
      --------------------------------------------------
      company_profiles.name AS company_name,
      company_profiles.currency,
      company_profiles.country,
      company_profiles.exchange,
      company_profiles.sector,
      company_profiles.industry,
      --------------------------------------------------
      -- Statistics
      --------------------------------------------------
      to_millions(statistics.market_capitalization) AS market_capitalization,
      statistics.beta,
      statistics.growth_estimate_next_year,
      statistics.short_percent,
      statistics.dividend_yield,
      statistics.most_recent_quarter,
      --------------------------------------------------
      -- income statement
      --------------------------------------------------
      income_statements.currency AS report_currency,
      to_millions(income_statements.total_revenue) AS revenue,
      to_millions(income_statements.gross_profit) AS gross_profit,
      -- profit margin
      ROUND(CASE WHEN total_revenue <> 0
            THEN gross_profit / total_revenue
            ELSE 0 END, 4) AS profit_margin,
      -- operating margins
      to_millions(income_statements.operating_income) AS operating_income,
      ROUND(CASE WHEN gross_profit <> 0
            THEN operating_income / gross_profit
            ELSE 0 END, 4) AS operating_margin,
      to_millions(income_statements.interest_expense) as interest_paid,
      ROUND(CASE WHEN operating_income <> 0
            THEN interest_expense / operating_income
            ELSE 0 END, 4) AS interest_to_operating_margin,
      -- income and taxes
      to_millions(income_statements.income_before_tax) AS income_before_tax,
      to_millions(income_statements.income_tax) AS income_tax,
      ROUND(CASE WHEN income_before_tax <> 0
            THEN income_tax / income_before_tax
            ELSE 0 END, 4) AS income_tax_rate,
      -- earnings
      to_millions(income_statements.net_earnings) AS earnings,

      --------------------------------------------------
      -- balance sheet
      --------------------------------------------------
      -- assets
      to_millions(balance_sheets.total_assets) AS assets,
      to_millions(balance_sheets.cash_and_short_term) AS cash,
      to_millions(balance_sheets.inventory) AS inventory,
      to_millions(balance_sheets.receivables) AS receivables,
      to_millions(balance_sheets.property_plant_equipment) AS property,
      to_millions(balance_sheets.good_will) AS good_will,
      to_millions(balance_sheets.long_term_investments) AS long_term_investments,
      ROUND(CASE WHEN balance_sheets.total_assets <> 0
            THEN income_statements.net_earnings / balance_sheets.total_assets
            ELSE 0 END, 4) AS return_on_assets,
      -- liabilities
      to_millions(balance_sheets.total_liabilities) AS liabilities,
      to_millions(balance_sheets.short_term_debt) AS short_term_debt,
      to_millions(balance_sheets.long_term_debt) AS long_term_debt,
      ROUND(CASE WHEN balance_sheets.total_stockholder_equity <> 0
            THEN balance_sheets.total_liabilities / balance_sheets.total_stockholder_equity
            ELSE 0 END, 4) AS debt_to_equity,
      to_millions(balance_sheets.total_capitalization) as capitalization,
      ROUND(CASE WHEN balance_sheets.total_capitalization - balance_sheets.cash_and_short_term <> 0
            THEN (income_statements.operating_income - income_statements.income_tax) /
                   (balance_sheets.total_capitalization - balance_sheets.cash_and_short_term)
            ELSE 0 END, 4) AS return_on_capital,
      -- equity
      to_millions(balance_sheets.total_stockholder_equity) AS equity,
      to_millions(balance_sheets.common_stock_equity) AS common_equity,
      to_millions(balance_sheets.preferred_stock_equity) AS preferred_equity,
      to_millions(balance_sheets.retained_earnings) AS retained_earnings,
      to_millions(balance_sheets.treasury_stock) AS treasury_stock,
      ROUND(CASE WHEN balance_sheets.total_stockholder_equity <> 0
            THEN income_statements.net_earnings / balance_sheets.total_stockholder_equity
            ELSE 0 END, 4) AS return_on_equity,
      --------------------------------------------------
      -- cash flow
      --------------------------------------------------
      to_millions(total_cash_from_operating_activities) AS cash_from_operating_activities,
      to_millions(total_cash_from_investing_activities) AS cash_from_investing_activities,
      to_millions(total_cash_from_financing_activities) AS cash_from_financing_activities,
      to_millions(cash_flow_statements.capital_expenditures) AS capital_expenditures,
      to_millions(free_cash_flow) AS free_cash_flow,
      ROUND(CASE WHEN income_statements.net_earnings <> 0
            THEN cash_flow_statements.capital_expenditures / income_statements.net_earnings
            ELSE 0 END, 4) AS capital_expenditures_to_earnings,
      to_millions(cash_flow_statements.sale_or_purchase_of_stock) AS stock_issuance,
      to_millions(-dividends_paid) AS dividends_paid,
      ROUND(CASE WHEN income_statements.net_earnings <> 0
            THEN -dividends_paid / income_statements.net_earnings
            ELSE 0 END, 4) AS dividends_rate,
      -- per share
      common_stock_shares_outstanding::bigint AS shares_outstanding,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN total_revenue / common_stock_shares_outstanding
            ELSE 0 END, 4) AS revenue_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN net_earnings / common_stock_shares_outstanding
            ELSE 0 END, 4) AS earnings_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN cash_and_short_term / common_stock_shares_outstanding
            ELSE 0 END, 4) AS cash_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN -dividends_paid / common_stock_shares_outstanding
            ELSE 0 END, 4) AS dividends_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN total_stockholder_equity / common_stock_shares_outstanding
            ELSE 0 END, 4) AS equity_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN free_cash_flow / common_stock_shares_outstanding
            ELSE 0 END, 4) AS cash_flow_per_share,
      EXISTS(SELECT 1 FROM errors WHERE errors.stock_id = stocks.id LIMIT 1) AS has_errors
    FROM stocks
        INNER JOIN company_profiles ON stocks.id = company_profiles.stock_id
        INNER JOIN statistics ON stocks.id = statistics.id
        INNER JOIN income_statements ON stocks.id = income_statements.stock_id
        INNER JOIN balance_sheets ON stocks.id = balance_sheets.stock_id
               AND income_statements.report_date = balance_sheets.report_date
               AND income_statements.report_type = balance_sheets.report_type
        INNER JOIN cash_flow_statements ON stocks.id = cash_flow_statements.stock_id
               AND income_statements.report_date = cash_flow_statements.report_date
               AND income_statements.report_type = cash_flow_statements.report_type
    WHERE stocks.active = 't'
    ORDER BY stocks.symbol, income_statements.report_type, income_statements.report_date desc
);

DROP MATERIALIZED VIEW IF EXISTS stock_general_report_with_growth;
CREATE MATERIALIZED VIEW stock_general_report_with_growth AS (
  SELECT
    stock_id,
    symbol,
    date,
    type,
    report_number,
    company_name,
    currency,
    country,
    sector,
    industry,
    market_capitalization,
    beta,
    growth_estimate_next_year,
    short_percent,
    dividend_yield,
    most_recent_quarter,
    report_currency,
    revenue,
    CASE WHEN report_number <> LAST_VALUE(report_number) OVER (
        PARTITION BY stock_id, symbol ORDER BY report_number
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) THEN growth(revenue, LAG(revenue) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS revenue_growth,
    gross_profit,
    profit_margin,
    operating_income,
    operating_margin,
    interest_paid,
    interest_to_operating_margin,
    income_before_tax,
    income_tax,
    income_tax_rate,
    earnings,
    CASE WHEN report_number <> LAST_VALUE(report_number) OVER (
        PARTITION BY stock_id, symbol ORDER BY report_number
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) THEN growth(earnings, LAG(earnings) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS earnings_growth,
    assets,
    CASE WHEN report_number <> LAST_VALUE(report_number) OVER (
        PARTITION BY stock_id, symbol ORDER BY report_number
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) THEN growth(assets, LAG(assets) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS assets_growth,
    cash,
    inventory,
    receivables,
    property,
    good_will,
    long_term_investments,
    return_on_assets,
    liabilities,
    CASE WHEN report_number <> LAST_VALUE(report_number) OVER (
        PARTITION BY stock_id, symbol ORDER BY report_number
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) THEN growth(liabilities, LAG(liabilities) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS liabilities_growth,
    short_term_debt,
    long_term_debt,
    debt_to_equity,
    capitalization,
    return_on_capital,
    equity,
    CASE WHEN report_number <> LAST_VALUE(report_number) OVER (
        PARTITION BY stock_id, symbol ORDER BY report_number
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) THEN growth(equity, LAG(equity) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS equity_growth,
    common_equity,
    preferred_equity,
    retained_earnings,
    treasury_stock,
    return_on_equity,
    cash_from_operating_activities,
    cash_from_investing_activities,
    cash_from_financing_activities,
    capital_expenditures,
    free_cash_flow,
    CASE WHEN report_number <> LAST_VALUE(report_number) OVER (
        PARTITION BY stock_id, symbol ORDER BY report_number
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) THEN growth(free_cash_flow, LAG(free_cash_flow) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS free_cash_flow_growth,
    capital_expenditures_to_earnings,
    stock_issuance,
    dividends_paid,
    dividends_rate,
    shares_outstanding,
    revenue_per_share,
    earnings_per_share,
    dividends_per_share,
    cash_per_share,
    equity_per_share,
    cash_flow_per_share,
    has_errors
  FROM stock_general_report
  ORDER BY date desc
);

DROP MATERIALIZED VIEW IF EXISTS stock_5y_report;
CREATE MATERIALIZED VIEW stock_5y_report AS (
    WITH years AS (
        SELECT
            *,
            SUM(dividends_per_share) OVER (PARTITION BY stock_id, symbol ORDER BY stock_id, date asc) AS accum_dividends_per_share,
            SUM(earnings_per_share) OVER (PARTITION BY stock_id, symbol ORDER BY stock_id, date asc) AS accum_eps
        FROM stock_general_report_with_growth
        WHERE report_number <= 5 AND type = 'Y'
    ),
    prices AS (
        SELECT
            dp.stock_id,
            y.date report_date,
            dp.adjusted_close AS close_price,
            dp.date AS price_date,
            RANK() OVER (PARTITION BY y.stock_id, y.date ORDER BY dp.date ASC) AS rank
        FROM years y
            INNER JOIN daily_prices dp ON y.stock_id = dp.stock_id
                                       AND dp.date BETWEEN y.date AND (y.date + interval '1 month')
    )
    SELECT
        y.*,
        CASE WHEN y.earnings_per_share <> 0 THEN ROUND(p.close_price / y.earnings_per_share, 3)
        ELSE 'NAN'::decimal END AS pe_ratio,
        p.close_price AS share_price,
        p.price_date
    FROM years y
        LEFT OUTER JOIN prices p ON p.stock_id = y.stock_id AND y.date = p.report_date AND rank = 1
    ORDER BY symbol, y.date ASC
);

DROP MATERIALIZED VIEW IF EXISTS stock_5y_averages;
CREATE MATERIALIZED VIEW stock_5y_averages AS (
    SELECT
        stock_5y_report.stock_id,
        symbol,
        company_name,
        market_capitalization,
        sector,
        industry,
        currencies.report_currency AS currency,
        MAX(date) last_report_date,
        ROUND(AVG(revenue_growth), 3) avg_revenue_growth,
        ROUND(MEDIAN(revenue_growth), 3) median_revenue_growth,
        ROUND(AVG(earnings_growth), 3) avg_earnings_growth,
        ROUND(MEDIAN(earnings_growth), 3) median_earnings_growth,
        ROUND(AVG(equity_growth), 3) avg_equity_growth,
        ROUND(MEDIAN(equity_growth), 3) median_equity_growth,
        ROUND(AVG(profit_margin), 3) avg_profit_margin,
        ROUND(AVG(return_on_assets), 3) avg_return_on_assets,
        ROUND(MEDIAN(return_on_assets), 3) median_return_on_assets,
        ROUND(AVG(return_on_capital), 3) avg_return_on_capital,
        ROUND(MEDIAN(return_on_capital), 3) median_return_on_capital,
        ROUND(AVG(return_on_equity), 3) avg_return_on_equity,
        ROUND(MEDIAN(return_on_equity), 3) median_return_on_equity,
        ROUND(AVG(dividends_rate), 3) avg_dividends_rate,
        ROUND(MEDIAN(dividends_rate), 3) median_dividends_rate,
        ROUND(AVG(free_cash_flow_growth), 3) avg_free_cash_flow_growth,
        ROUND(MEDIAN(free_cash_flow_growth), 3) median_free_cash_flow_growth,
        ROUND(AVG(pe_ratio) FILTER (WHERE pe_ratio >= 0), 3) AS avg_pe_ratio,
        ROUND(MAX(pe_ratio) FILTER (WHERE pe_ratio >= 0), 3) max_pe_ratio,
        ROUND(MIN(pe_ratio) FILTER (WHERE pe_ratio >= 0), 3) AS min_pe_ratio,
        ROUND(
            -REGR_SLOPE(
                earnings::decimal,
                (report_number - 1)::decimal
            )::decimal
        , 3) earnings_trend,
        COUNT(*) years,
        EXISTS(SELECT 1 FROM errors WHERE errors.stock_id = stock_5y_report.stock_id LIMIT 1) AS has_errors
    FROM stock_5y_report
        INNER JOIN (
            SELECT
                stock_id,
                report_currency,
                RANK() OVER (PARTITION BY stock_id ORDER BY COUNT(*) DESC) rank
            FROM stock_5y_report
            GROUP BY stock_id, report_currency
        ) AS currencies ON currencies.stock_id = stock_5y_report.stock_id AND currencies.rank = 1
    GROUP BY stock_5y_report.stock_id, symbol, company_name, market_capitalization, sector, industry, currencies.report_currency
);

DROP VIEW IF EXISTS stock_buffettology_report;
CREATE VIEW stock_buffettology_report AS (
    WITH five_year_old_stocks AS (
      SELECT DISTINCT stock_id FROM stock_5y_report WHERE report_number = 5
    ),
    latest_prices AS (
        SELECT
            stock_id,
            adjusted_close AS close_price,
            date AS price_date,
            RANK() OVER (PARTITION BY stock_id ORDER BY date DESC) AS rank
        FROM daily_prices
        WHERE adjusted_close <> 0
    ),
    per_share AS (
        SELECT DISTINCT
           stock_id,
           symbol,
           (NTH_VALUE(accum_dividends_per_share, 2) OVER (
               PARTITION BY stock_id, symbol ORDER BY report_number
               RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ))::decimal prev_accum_dividends,
           (NTH_VALUE(accum_eps, 2) OVER (
               PARTITION BY stock_id, symbol ORDER BY report_number
               RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ))::decimal prev_accum_eps,
           (FIRST_VALUE(accum_dividends_per_share) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal accum_dividends,
           (FIRST_VALUE(accum_eps) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal accum_eps,
           (FIRST_VALUE(equity_per_share) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal equity_per_share,
           (FIRST_VALUE(dividends_per_share) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal dividends,
           (FIRST_VALUE(earnings_per_share) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal eps,
           (NTH_VALUE(earnings_per_share, 5) OVER (
               PARTITION BY stock_id, symbol ORDER BY report_number
               RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ))::decimal eps_5y,
           (FIRST_VALUE(earnings) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal earnings,
           (NTH_VALUE(earnings, 5) OVER (
               PARTITION BY stock_id, symbol ORDER BY report_number
               RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ))::decimal earnings_5y,
           (FIRST_VALUE(free_cash_flow) OVER (PARTITION BY stock_id, symbol ORDER BY report_number))::decimal free_cash_flow,
           (NTH_VALUE(free_cash_flow, 5) OVER (
               PARTITION BY stock_id, symbol ORDER BY report_number
               RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ))::decimal free_cash_flow_5y,
           (FIRST_VALUE(date) OVER (PARTITION BY stock_id, symbol ORDER BY report_number)) last_report_date
        FROM stock_5y_report
    ),
    currencies AS (
        SELECT
            stock_id,
            currency,
            report_date,
            report_type,
            RANK() OVER (PARTITION BY stock_id, report_type ORDER BY stock_id, report_type, report_date DESC) AS rank
        FROM income_statements
        WHERE report_type = 'Y'
    ),
    base AS (
        SELECT
            averages.stock_id,
            averages.symbol,
            averages.company_name,
            company_profiles.url,
            'https://finance.yahoo.com/quote/' || averages.symbol AS yahoo_url,
            company_profiles.logo_url,
            averages.market_capitalization AS market_cap,
            averages.sector,
            averages.industry,
            company_profiles.category,
            currencies.currency,
            averages.has_errors,
            per_share.last_report_date,
            averages.earnings_trend,
            averages.median_earnings_growth,
            averages.median_equity_growth,
            averages.median_return_on_equity,
            averages.median_dividends_rate,
            per_share.equity_per_share,
            per_share.dividends,
            per_share.eps,
            per_share.eps_5y,
            per_share.earnings,
            per_share.earnings_5y,
            per_share.free_cash_flow,
            per_share.free_cash_flow_5y,
            CAGR(per_share.eps, per_share.eps_5y, 5) AS eps_cagr_5y,
            CAGR(per_share.earnings, per_share.earnings_5y, 5) AS earnings_cagr_5y,
            CAGR(per_share.free_cash_flow, per_share.free_cash_flow_5y, 5) AS free_cash_flow_cagr_5y,
            per_share.accum_dividends,
            per_share.accum_eps,
            CASE
              WHEN (per_share.prev_accum_eps - per_share.prev_accum_dividends) <> 0 THEN ROUND((per_share.eps - per_share.eps_5y) / (per_share.prev_accum_eps - per_share.prev_accum_dividends), 3)
              ELSE 'NaN'::decimal END AS return_on_retained_earnings,
            latest_prices.close_price AS last_price,
            latest_prices.price_date,
            CASE
              WHEN per_share.eps <> 0 THEN ROUND(latest_prices.close_price / per_share.eps, 3)
              ELSE 'NaN'::decimal END AS pe_ratio,
            averages.avg_pe_ratio AS avg_pe_ratio,
            averages.min_pe_ratio AS min_pe_ratio,
            CASE
              WHEN latest_prices.close_price <> 0 THEN ROUND(per_share.eps / latest_prices.close_price, 3)
              ELSE 'NaN'::decimal END AS rate_of_return
        FROM five_year_old_stocks st
            INNER JOIN stock_5y_averages AS averages ON averages.stock_id = st.stock_id
            INNER JOIN latest_prices ON latest_prices.stock_id = st.stock_id AND latest_prices.rank = 1
            INNER JOIN currencies ON currencies.stock_id = st.stock_id AND currencies.rank = 1
            INNER JOIN per_share ON per_share.stock_id = st.stock_id
            INNER JOIN company_profiles ON company_profiles.stock_id = st.stock_id
        WHERE per_share.eps <> 0
    ),
    estimations AS (
        SELECT
            base.symbol,
            base.eps *
                POWER(1 + base.eps_cagr_5y, 3) *
                POWER(1 + base.eps_cagr_5y * 0.75, 1) *
                POWER(1 + base.eps_cagr_5y * 0.50, 1) AS estimated_eps
         FROM base
    ),
    results AS (
        SELECT
            base.*,
            ROUND(estimations.estimated_eps, 3) estimated_eps,
            ROUND(estimations.estimated_eps * base.median_return_on_equity, 3) AS estimated_equity_per_share,
            ROUND(estimations.estimated_eps / base.last_price, 3) AS estimated_rate_of_return,
            ROUND(estimations.estimated_eps * base.avg_pe_ratio, 3) AS estimated_price_avg_pe,
            ROUND(estimations.estimated_eps * base.min_pe_ratio, 3) AS estimated_price_min_pe,
            CAGR(estimations.estimated_eps * base.avg_pe_ratio, base.last_price, 5) AS roi_avg_pe,
            CAGR(estimations.estimated_eps * base.min_pe_ratio, base.last_price, 5) AS roi_min_pe
        FROM base
            INNER JOIN estimations on estimations.symbol = base.symbol
    )
    SELECT * FROM results
);

DROP VIEW IF EXISTS stock_simple_analysis;
CREATE VIEW stock_simple_analysis AS (
    SELECT
        sb.symbol,
        logo_url,
        company_name company,
        industry,
        last_report_date reported_date,
        roi_min_pe annual_return,
        last_price AS share_price,
        dcf.discounted_share_price AS dcf_price,
        ROUND((dcf.discounted_share_price / last_price) - 1, 3) AS margin,
        eps,
        eps_5y,
        rate_of_return,
        return_on_retained_earnings,
        eps_cagr_5y cagr,
        median_earnings_growth earnings_growth,
        pe_ratio,
        avg_pe_ratio,
        min_pe_ratio,
        estimated_eps,
        estimated_rate_of_return,
        estimated_price_min_pe AS estimated_price
    FROM stock_buffettology_report sb
        LEFT OUTER JOIN discounted_cash_flows dcf ON
             dcf.stock_id = sb.stock_id AND dcf.discount_rate = 0.15
    WHERE earnings_trend > 0
      AND eps_cagr_5y > 0
      AND eps_cagr_5y <> 'NAN'::decimal
      AND has_errors = 'f'
      AND currency = 'USD'
      AND category ILIKE '%domestic%'
      AND median_return_on_equity > 0
      AND median_equity_growth > 0
      AND median_earnings_growth > 0
      AND return_on_retained_earnings > 0
);

DROP VIEW IF EXISTS stock_dcf_analysis;
CREATE VIEW stock_dcf_analysis AS (
    SELECT
        s.symbol,
        cp.name,
        cp.industry,
        dcf.discount_rate,
        dp.price,
        dcf.discounted_share_price discounted_price,
        ROUND((dcf.discounted_share_price / dp.price) - 1, 3) margin
    FROM discounted_cash_flows dcf
        INNER JOIN (
              SELECT
                  stock_id,
                  adjusted_close price,
                  date
              FROM daily_prices WHERE adjusted_close <> 0
        ) dp ON dp.stock_id = dcf.stock_id
        INNER JOIN (
            SELECT stock_id, MAX(date) max_date FROM daily_prices WHERE adjusted_close <> 0 GROUP BY stock_id
        ) dp2 ON dp2.stock_id = dp.stock_id AND dp2.max_date = dp.date
        INNER JOIN stocks s ON s.id = dcf.stock_id
        INNER JOIN company_profiles cp ON s.id = cp.stock_id
        INNER JOIN (
            SELECT
                stock_id,
                currency,
                RANK() OVER (PARTITION BY stock_id, report_type ORDER BY stock_id, report_type, report_date DESC) AS rank
            FROM income_statements
            WHERE report_type = 'Y'
        ) currencies ON currencies.stock_id = s.id AND currencies.rank = 1
    WHERE dcf.discounted_share_price > dp.price
      AND dcf.discounted_share_price <> 'NAN'::DECIMAL
      AND dcf.stock_id NOT IN (SELECT DISTINCT stock_id FROM errors)
      AND currencies.currency = 'USD'
      AND category ILIKE '%domestic%'
    ORDER BY s.symbol, dcf.discount_rate DESC
);
