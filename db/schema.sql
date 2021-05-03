--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6 (Ubuntu 12.6-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.6 (Ubuntu 12.6-0ubuntu0.20.10.1)

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
-- Name: companies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    stock_id integer NOT NULL,
    name text,
    cik text,
    description text,
    address text,
    country text,
    currency text,
    sector text,
    industry text,
    fulltime_employees bigint,
    deleted_at timestamp(6) without time zone,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Name: migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.migrations (
    migration character varying(255) NOT NULL,
    batch integer NOT NULL
);


--
-- Name: stocks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stocks (
    id integer NOT NULL,
    symbol text NOT NULL,
    name text NOT NULL,
    deleted_at timestamp(6) without time zone,
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
-- Name: summaries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.summaries (
    id integer NOT NULL,
    stock_id integer NOT NULL,
    latest_quarter date NOT NULL,
    market_capitalization bigint,
    beta numeric(16,4),
    book_value numeric(16,4),
    ebitda bigint,
    eps numeric(16,4),
    ev_to_ebitda numeric(16,4),
    ev_to_revenue numeric(16,4),
    forward_pe numeric(16,4),
    pe_ratio numeric(16,4),
    peg_ratio numeric(16,4),
    price_to_book_ratio numeric(16,4),
    profit_margin numeric(16,4),
    trailing_pe numeric(16,4),
    diluted_eps_ttm numeric(16,4),
    gross_profit_ttm bigint,
    operating_margin_ttm numeric(16,4),
    price_to_sales_ratio_ttm numeric(16,4),
    quaterly_earnings_growth_yoy numeric(16,4),
    quaterly_revenue_growth_yoy numeric(16,4),
    return_on_assets_ttm numeric(16,4),
    return_on_equity_ttm numeric(16,4),
    revenue_per_share_ttm numeric(16,4),
    revenue_ttm bigint,
    "200_day_moving_average" numeric(16,4),
    "50_day_moving_average" numeric(16,4),
    "52_week_high" numeric(16,4),
    "52_week_low" numeric(16,4),
    shares_float bigint,
    shares_outstanding bigint,
    shares_short bigint,
    shares_short_prior_month bigint,
    short_ratio numeric(16,4),
    short_percent_outstanding numeric(16,4),
    short_percent_float numeric(16,4),
    dividend_per_share numeric(16,4),
    dividend_yield numeric(16,4),
    payout_ratio numeric(16,4),
    forward_annual_dividend_rate numeric(16,4),
    forward_annual_dividend_yield numeric(16,4),
    dividend_date date,
    ex_dividend_date date,
    last_split_factor text,
    last_split_date date,
    analyst_target_price numeric(16,4),
    percent_insiders numeric(16,4),
    percent_institutions numeric(16,4),
    deleted_at timestamp(6) without time zone,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP(6) NOT NULL
);


--
-- Name: summaries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.summaries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: summaries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.summaries_id_seq OWNED BY public.summaries.id;


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: stocks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks ALTER COLUMN id SET DEFAULT nextval('public.stocks_id_seq'::regclass);


--
-- Name: summaries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.summaries ALTER COLUMN id SET DEFAULT nextval('public.summaries_id_seq'::regclass);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


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
-- Name: summaries summaries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.summaries
    ADD CONSTRAINT summaries_pkey PRIMARY KEY (id);


--
-- Name: summaries summaries_stock_id_latest_quarter_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.summaries
    ADD CONSTRAINT summaries_stock_id_latest_quarter_unique UNIQUE (stock_id, latest_quarter);


--
-- Name: companies_stock_id_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX companies_stock_id_index ON public.companies USING btree (stock_id);


--
-- Name: companies companies_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- Name: summaries summaries_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.summaries
    ADD CONSTRAINT summaries_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6 (Ubuntu 12.6-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.6 (Ubuntu 12.6-0ubuntu0.20.10.1)

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
INSERT INTO public.migrations VALUES ('2021_05_01_173849_create_companies_table', 1);
INSERT INTO public.migrations VALUES ('2021_05_02_014835_create_summaries_table', 1);


--
-- PostgreSQL database dump complete
--

