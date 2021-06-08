--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Ubuntu 12.7-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.7 (Ubuntu 12.7-0ubuntu0.20.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: balance_sheets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.balance_sheets (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    report_date date NOT NULL,
    report_type character(2) NOT NULL,
    currency text,
    filing_date date NOT NULL,
    total_assets numeric(20,5) NOT NULL,
    total_current_assets numeric(20,5) NOT NULL,
    cash_and_short_term numeric(20,5) NOT NULL,
    inventory numeric(20,5) NOT NULL,
    receivables numeric(20,5) NOT NULL,
    other_current_assets numeric(20,5) NOT NULL,
    total_non_current_assets numeric(20,5) NOT NULL,
    property_plant_equipment numeric(20,5) NOT NULL,
    good_will numeric(20,5) NOT NULL,
    intangible_assets numeric(20,5) NOT NULL,
    long_term_investments numeric(20,5) NOT NULL,
    other_non_current_assets numeric(20,5) NOT NULL,
    total_liabilities numeric(20,5) NOT NULL,
    total_current_liabilities numeric(20,5) NOT NULL,
    accounts_payable numeric(20,5) NOT NULL,
    short_term_debt numeric(20,5) NOT NULL,
    other_current_liabilities numeric(20,5) NOT NULL,
    total_non_current_liabilities numeric(20,5) NOT NULL,
    long_term_debt numeric(20,5) NOT NULL,
    deferred_long_term_liabilities numeric(20,5) NOT NULL,
    other_non_current_liabilities numeric(20,5) NOT NULL,
    total_stockholder_equity numeric(20,5) NOT NULL,
    preferred_stock_equity numeric(20,5) NOT NULL,
    common_stock_equity numeric(20,5) NOT NULL,
    paid_in_capital numeric(20,5) NOT NULL,
    retained_earnings numeric(20,5) NOT NULL,
    treasury_stock numeric(20,5) NOT NULL,
    gain_losses numeric(20,5) NOT NULL,
    non_controlling_interest numeric(20,5) NOT NULL,
    total_capitalization numeric(20,5) NOT NULL,
    capital_lease_obligations numeric(20,5) NOT NULL,
    net_tangible_assets numeric(20,5) NOT NULL,
    net_working_capital numeric(20,5) NOT NULL,
    net_invested_capital numeric(20,5) NOT NULL,
    short_long_term_debt_total numeric(20,5) NOT NULL,
    net_debt numeric(20,5) NOT NULL,
    common_stock_shares_outstanding numeric(20,5) NOT NULL,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: balance_sheets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.balance_sheets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: balance_sheets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.balance_sheets_id_seq OWNED BY public.balance_sheets.id;


--
-- Name: cash_flow_statements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cash_flow_statements (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    report_date date NOT NULL,
    report_type character(2) NOT NULL,
    currency text,
    filing_date date NOT NULL,
    net_income numeric(20,5) NOT NULL,
    depreciation numeric(20,5) NOT NULL,
    other_cash_from_operating_activites numeric(20,5) NOT NULL,
    total_cash_from_operating_activities numeric(20,5) NOT NULL,
    capital_expenditures numeric(20,5) NOT NULL,
    investments numeric(20,5) NOT NULL,
    other_cash_from_investing_activities numeric(20,5) NOT NULL,
    total_cash_from_investing_activities numeric(20,5) NOT NULL,
    net_borrowing numeric(20,5) NOT NULL,
    dividends_paid numeric(20,5) NOT NULL,
    sale_or_purchase_of_stock numeric(20,5) NOT NULL,
    other_cash_from_financing_activities numeric(20,5) NOT NULL,
    total_cash_from_financing_activities numeric(20,5) NOT NULL,
    initial_cash numeric(20,5) NOT NULL,
    change_in_cash numeric(20,5) NOT NULL,
    final_cash numeric(20,5) NOT NULL,
    free_cash_flow numeric(20,5) NOT NULL,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: cash_flow_statements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cash_flow_statements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cash_flow_statements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cash_flow_statements_id_seq OWNED BY public.cash_flow_statements.id;


--
-- Name: company_profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.company_profiles (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    address text NOT NULL,
    phone text NOT NULL,
    url text NOT NULL,
    logo_url text NOT NULL,
    exchange text NOT NULL,
    currency text NOT NULL,
    country text NOT NULL,
    location text NOT NULL,
    sector text NOT NULL,
    industry text NOT NULL,
    category text NOT NULL,
    isin text,
    cusip text,
    cik text,
    is_delisted boolean NOT NULL,
    fulltime_employees bigint NOT NULL,
    ipo_date date,
    last_update_date date,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: company_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.company_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: company_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.company_profiles_id_seq OWNED BY public.company_profiles.id;


--
-- Name: daily_prices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.daily_prices (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    date date NOT NULL,
    open numeric(20,4) NOT NULL,
    high numeric(20,4) NOT NULL,
    low numeric(20,4) NOT NULL,
    close numeric(20,4) NOT NULL,
    adjusted_close numeric(20,4) NOT NULL,
    volume bigint NOT NULL,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: daily_prices_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.daily_prices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: daily_prices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.daily_prices_id_seq OWNED BY public.daily_prices.id;


--
-- Name: errors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.errors (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    message text NOT NULL,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: errors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.errors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: errors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.errors_id_seq OWNED BY public.errors.id;


--
-- Name: income_statements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.income_statements (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    report_date date NOT NULL,
    report_type character(2) NOT NULL,
    currency text,
    filing_date date NOT NULL,
    total_revenue numeric(20,5) NOT NULL,
    cost_of_revenue numeric(20,5) NOT NULL,
    gross_profit numeric(20,5) NOT NULL,
    operating_expenses numeric(20,5) NOT NULL,
    sga_expense numeric(20,5) NOT NULL,
    research_and_development numeric(20,5) NOT NULL,
    depreciation_and_amortization numeric(20,5) NOT NULL,
    operating_income numeric(20,5) NOT NULL,
    interest_expense numeric(20,5) NOT NULL,
    interest_income numeric(20,5) NOT NULL,
    other_expenses numeric(20,5) NOT NULL,
    income_before_tax numeric(20,5) NOT NULL,
    income_tax numeric(20,5) NOT NULL,
    net_income_after_tax numeric(20,5) NOT NULL,
    discontinued_operations numeric(20,5) NOT NULL,
    net_earnings numeric(20,5) NOT NULL,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: income_statements_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.income_statements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: income_statements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.income_statements_id_seq OWNED BY public.income_statements.id;


--
-- Name: migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.migrations (
    migration character varying(255) NOT NULL,
    batch integer NOT NULL
);


--
-- Name: statistics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.statistics (
    id bigint NOT NULL,
    stock_id integer NOT NULL,
    market_capitalization numeric(20,5) NOT NULL,
    wallstreet_target_price numeric(20,5) NOT NULL,
    pe_ratio numeric(20,5) NOT NULL,
    peg_ratio numeric(20,5) NOT NULL,
    book_value_per_share numeric(20,5) NOT NULL,
    earnings_per_share numeric(20,5) NOT NULL,
    dividend_per_share numeric(20,5) NOT NULL,
    dividend_yield numeric(20,5) NOT NULL,
    profit_margin numeric(20,5) NOT NULL,
    diluted_eps_ttm numeric(20,5) NOT NULL,
    gross_profit_ttm numeric(20,5) NOT NULL,
    price_to_sales_ttm numeric(20,5) NOT NULL,
    operating_margin_ttm numeric(20,5) NOT NULL,
    return_on_assets_ttm numeric(20,5) NOT NULL,
    return_on_equity_ttm numeric(20,5) NOT NULL,
    revenue_per_share_ttm numeric(20,5) NOT NULL,
    revenue_ttm numeric(20,5) NOT NULL,
    price_to_book_mrq numeric(20,5) NOT NULL,
    quarterly_revenue_growth_yoy numeric(20,5) NOT NULL,
    quarterly_earnings_growth_yoy numeric(20,5) NOT NULL,
    outstanding_shares numeric(20,5) NOT NULL,
    floating_shares numeric(20,5) NOT NULL,
    percent_insiders numeric(20,5) NOT NULL,
    percent_institutions numeric(20,5) NOT NULL,
    short_ratio numeric(20,5) NOT NULL,
    short_percent numeric(20,5) NOT NULL,
    beta numeric(20,5) NOT NULL,
    eps_estimate_current_year numeric(20,5) NOT NULL,
    eps_estimate_next_year numeric(20,5) NOT NULL,
    eps_estimate_current_quarter numeric(20,5) NOT NULL,
    eps_estimate_next_quarter numeric(20,5) NOT NULL,
    growth_estimate_current_quarter numeric(20,5) NOT NULL,
    growth_estimate_current_year numeric(20,5) NOT NULL,
    growth_estimate_next_year numeric(20,5) NOT NULL,
    most_recent_quarter date,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: statistics_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.statistics_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: statistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.statistics_id_seq OWNED BY public.statistics.id;


--
-- Name: stocks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stocks (
    id integer NOT NULL,
    symbol text NOT NULL,
    name text NOT NULL,
    country text NOT NULL,
    currency text NOT NULL,
    exchange text NOT NULL,
    active boolean NOT NULL,
    source text NOT NULL,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: stocks_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stocks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: stocks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stocks_id_seq OWNED BY public.stocks.id;


--
-- Name: balance_sheets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.balance_sheets ALTER COLUMN id SET DEFAULT nextval('public.balance_sheets_id_seq'::regclass);


--
-- Name: cash_flow_statements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_flow_statements ALTER COLUMN id SET DEFAULT nextval('public.cash_flow_statements_id_seq'::regclass);


--
-- Name: company_profiles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company_profiles ALTER COLUMN id SET DEFAULT nextval('public.company_profiles_id_seq'::regclass);


--
-- Name: daily_prices id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_prices ALTER COLUMN id SET DEFAULT nextval('public.daily_prices_id_seq'::regclass);


--
-- Name: errors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.errors ALTER COLUMN id SET DEFAULT nextval('public.errors_id_seq'::regclass);


--
-- Name: income_statements id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.income_statements ALTER COLUMN id SET DEFAULT nextval('public.income_statements_id_seq'::regclass);


--
-- Name: statistics id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics ALTER COLUMN id SET DEFAULT nextval('public.statistics_id_seq'::regclass);


--
-- Name: stocks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks ALTER COLUMN id SET DEFAULT nextval('public.stocks_id_seq'::regclass);


--
-- Name: balance_sheets balance_sheets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.balance_sheets
    ADD CONSTRAINT balance_sheets_pkey PRIMARY KEY (id);


--
-- Name: balance_sheets balance_sheets_stock_id_report_date_report_type_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.balance_sheets
    ADD CONSTRAINT balance_sheets_stock_id_report_date_report_type_unique UNIQUE (stock_id, report_date, report_type);


--
-- Name: cash_flow_statements cash_flow_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_flow_statements
    ADD CONSTRAINT cash_flow_statements_pkey PRIMARY KEY (id);


--
-- Name: cash_flow_statements cash_flow_statements_stock_id_report_date_report_type_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_flow_statements
    ADD CONSTRAINT cash_flow_statements_stock_id_report_date_report_type_unique UNIQUE (stock_id, report_date, report_type);


--
-- Name: company_profiles company_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company_profiles
    ADD CONSTRAINT company_profiles_pkey PRIMARY KEY (id);


--
-- Name: company_profiles company_profiles_stock_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company_profiles
    ADD CONSTRAINT company_profiles_stock_id_unique UNIQUE (stock_id);


--
-- Name: daily_prices daily_prices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_prices
    ADD CONSTRAINT daily_prices_pkey PRIMARY KEY (id);


--
-- Name: daily_prices daily_prices_stock_id_date_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_prices
    ADD CONSTRAINT daily_prices_stock_id_date_unique UNIQUE (stock_id, date);


--
-- Name: errors errors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_pkey PRIMARY KEY (id);


--
-- Name: income_statements income_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.income_statements
    ADD CONSTRAINT income_statements_pkey PRIMARY KEY (id);


--
-- Name: income_statements income_statements_stock_id_report_date_report_type_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.income_statements
    ADD CONSTRAINT income_statements_stock_id_report_date_report_type_unique UNIQUE (stock_id, report_date, report_type);


--
-- Name: statistics statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_pkey PRIMARY KEY (id);


--
-- Name: statistics statistics_stock_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_stock_id_unique UNIQUE (stock_id);


--
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (id);


--
-- Name: stocks stocks_symbol_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_symbol_unique UNIQUE (symbol);


--
-- Name: daily_prices_date_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX daily_prices_date_index ON public.daily_prices USING btree (date);


--
-- Name: errors_stock_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX errors_stock_id_index ON public.errors USING btree (stock_id);


--
-- Name: balance_sheets balance_sheets_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.balance_sheets
    ADD CONSTRAINT balance_sheets_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: cash_flow_statements cash_flow_statements_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_flow_statements
    ADD CONSTRAINT cash_flow_statements_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: company_profiles company_profiles_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company_profiles
    ADD CONSTRAINT company_profiles_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: daily_prices daily_prices_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_prices
    ADD CONSTRAINT daily_prices_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: errors errors_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: income_statements income_statements_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.income_statements
    ADD CONSTRAINT income_statements_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: statistics statistics_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Ubuntu 12.7-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.7 (Ubuntu 12.7-0ubuntu0.20.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: migrations; Type: TABLE DATA; Schema: public; Owner: stocks
--

INSERT INTO public.migrations VALUES ('2021_05_01_024853_create_stocks_table', 1);
INSERT INTO public.migrations VALUES ('2021_05_09_035031_create_daily_prices_table', 2);
INSERT INTO public.migrations VALUES ('2021_05_10_052729_create_income_statements_table', 3);
INSERT INTO public.migrations VALUES ('2021_05_21_180714_create_balance_sheets_table', 3);
INSERT INTO public.migrations VALUES ('2021_05_22_023340_create_cash_flow_statements_table', 3);
INSERT INTO public.migrations VALUES ('2021_05_25_035928_create_companies_table', 4);
INSERT INTO public.migrations VALUES ('2021_05_27_210259_create_table_data_errors', 5);
INSERT INTO public.migrations VALUES ('2021_06_03_044026_create_statistics_table', 6);


--
-- PostgreSQL database dump complete
--

