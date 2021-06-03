DROP MATERIALIZED VIEW IF EXISTS stock_yearly_averages;
DROP MATERIALIZED VIEW IF EXISTS stock_general_report_with_growth;
DROP MATERIALIZED VIEW IF EXISTS stock_general_report;

DROP MATERIALIZED VIEW IF EXISTS stock_general_report;
CREATE OR REPLACE FUNCTION growth(after DECIMAL, before DECIMAL) RETURNS DECIMAL AS $$
BEGIN
  RETURN CASE
    WHEN before <> 0 THEN ROUND((after - before) / ABS(before), 2)
    ELSE 0 END;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION to_millions(amount DECIMAL) RETURNS DECIMAL AS $$
BEGIN
  RETURN ROUND(amount/1000000,2);
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
      RANK() OVER (PARTITION BY stocks.symbol, income_statements.report_type ORDER BY income_statements.report_date) AS report_number,
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
      -- income statement
      --------------------------------------------------
      to_millions(income_statements.total_revenue) AS revenue,
      to_millions(income_statements.gross_profit) AS gross_profit,
      -- profit margin
      ROUND(CASE WHEN total_revenue <> 0
            THEN gross_profit / total_revenue
            ELSE 0 END, 4) AS profit_margin,
      -- expenses ratios
      ROUND(CASE WHEN gross_profit <> 0
            THEN sga_expense / gross_profit
            ELSE 0 END, 4) AS sga_to_profit,
      ROUND(CASE WHEN gross_profit <> 0
            THEN research_and_development / gross_profit
            ELSE 0 END, 4) AS rd_to_profit,
      ROUND(CASE WHEN gross_profit <> 0
            THEN depreciation_and_amortization / gross_profit
            ELSE 0 END, 4) AS depreciation_to_profit,
      -- operating margins
      to_millions(income_statements.operating_income) AS operating_income,
      ROUND(CASE WHEN gross_profit <> 0
            THEN operating_income / gross_profit
            ELSE 0 END, 4) AS operating_margin,
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
      ROUND(CASE WHEN total_revenue <> 0
            THEN balance_sheets.receivables / total_revenue
            ELSE 0 END, 4) AS receivables_to_sales,
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
      ROUND(CASE WHEN income_statements.net_earnings <> 0
            THEN balance_sheets.long_term_debt / income_statements.net_earnings
            ELSE 0 END, 4) AS years_to_pay,
      ROUND(CASE WHEN balance_sheets.total_stockholder_equity <> 0
            THEN balance_sheets.total_liabilities / balance_sheets.total_stockholder_equity
            ELSE 0 END, 4) AS debt_to_equity,
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
      to_millions(cash_flow_statements.capital_expenditures) AS capital_expenditures,
      ROUND(CASE WHEN income_statements.net_earnings <> 0
            THEN cash_flow_statements.capital_expenditures / income_statements.net_earnings
            ELSE 0 END, 4) AS capital_expenditures_to_earnings,
      to_millions(cash_flow_statements.sale_or_purchase_of_stock) AS stock_issuance,
      to_millions(-cash_flow_statements.dividends_paid) AS dividends_paid,
      -- per share
      common_stock_shares_outstanding::bigint AS shares_outstanding,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN total_revenue / common_stock_shares_outstanding
            ELSE 0 END, 4) AS revenue_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN income_before_tax / common_stock_shares_outstanding
            ELSE 0 END, 4) AS earnings_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN cash_and_short_term / common_stock_shares_outstanding
            ELSE 0 END, 4) AS cash_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN dividends_paid / common_stock_shares_outstanding
            ELSE 0 END, 4) AS dividends_per_share,
      ROUND(CASE WHEN common_stock_shares_outstanding <> 0
            THEN total_stockholder_equity / common_stock_shares_outstanding
            ELSE 0 END, 4) AS equity_per_share
    FROM stocks
      LEFT OUTER JOIN company_profiles ON stocks.id = company_profiles.stock_id
      INNER JOIN income_statements ON stocks.id = income_statements.stock_id
      INNER JOIN balance_sheets ON stocks.id = balance_sheets.stock_id
             AND income_statements.report_date = balance_sheets.report_date
             AND income_statements.report_type = balance_sheets.report_type
      INNER JOIN cash_flow_statements ON stocks.id = cash_flow_statements.stock_id
             AND income_statements.report_date = cash_flow_statements.report_date
             AND income_statements.report_type = cash_flow_statements.report_type
    WHERE stocks.id NOT IN (SELECT DISTINCT stock_id FROM errors)
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
    revenue,
    CASE WHEN report_number <> 1
    THEN growth(revenue, LAG(revenue) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS revenue_growth,
    gross_profit,
    profit_margin,
    sga_to_profit,
    rd_to_profit,
    depreciation_to_profit,
    operating_income,
    operating_margin,
    interest_to_operating_margin,
    income_before_tax,
    income_tax,
    income_tax_rate,
    earnings,
    CASE WHEN report_number <> 1
    THEN growth(earnings, LAG(earnings) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS earnings_growth,
    assets,
    CASE WHEN report_number <> 1
    THEN growth(assets, LAG(assets) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS assets_growth,
    cash,
    inventory,
    receivables,
    receivables_to_sales,
    property,
    good_will,
    long_term_investments,
    return_on_assets,
    liabilities,
    CASE WHEN report_number <> 1
    THEN growth(liabilities, LAG(liabilities) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS liabilities_growth,
    short_term_debt,
    long_term_debt,
    years_to_pay,
    debt_to_equity,
    equity,
    CASE WHEN report_number <> 1
    THEN growth(equity, LAG(equity) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS equity_growth,
    common_equity,
    preferred_equity,
    retained_earnings,
    CASE WHEN report_number <> 1
    THEN growth(retained_earnings, LAG(retained_earnings) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS retained_earnings_growth,
    treasury_stock,
    return_on_equity,
    capital_expenditures,
    CASE WHEN report_number <> 1
    THEN growth(capital_expenditures, LAG(capital_expenditures) OVER (ORDER BY symbol, type, date))
    ELSE 0 END AS capital_expenditures_growth,
    capital_expenditures_to_earnings,
    stock_issuance,
    dividends_paid,
    shares_outstanding,
    revenue_per_share,
    earnings_per_share,
    dividends_per_share,
    cash_per_share,
    equity_per_share
  FROM stock_general_report
  ORDER BY symbol, type, date desc
);

DROP MATERIALIZED VIEW IF EXISTS stock_yearly_averages;
CREATE MATERIALIZED VIEW stock_yearly_averages AS (
    SELECT
        stock_id,
        symbol,
        company_name,
        sector,
        industry,
        ROUND(AVG(revenue_growth),2) avg_revenue_growth,
        ROUND(AVG(earnings_growth),2) avg_earnings_growth,
        ROUND(AVG(equity_growth),2) avg_equity_growth,
        ROUND(AVG(profit_margin),2) avg_profit_margin,
        ROUND(AVG(return_on_assets),2) avg_return_on_assets,
        ROUND(AVG(return_on_equity),2) avg_return_on_equity,
        ROUND(
            REGR_SLOPE(
                earnings::decimal,
                (report_number - 1)::decimal
            )::decimal
        , 3) trend,
        COUNT(*) years
    FROM stock_general_report_with_growth
    WHERE type = 'Y'
    GROUP BY stock_id, symbol, company_name, sector, industry
);
