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
    dividends numeric(20,4) DEFAULT 0.0 NOT NULL,
    split_coefficient numeric(20,4) DEFAULT 1.0 NOT NULL,
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
    ticker text NOT NULL,
    name text NOT NULL,
    locale text NOT NULL,
    currency text NOT NULL,
    exchange text NOT NULL,
    cik text NOT NULL,
    active boolean NOT NULL,
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
-- Name: daily_prices id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_prices ALTER COLUMN id SET DEFAULT nextval('public.daily_prices_id_seq'::regclass);


--
-- Name: stocks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks ALTER COLUMN id SET DEFAULT nextval('public.stocks_id_seq'::regclass);


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
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (id);


--
-- Name: stocks stocks_ticker_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_ticker_unique UNIQUE (ticker);


--
-- Name: daily_prices_date_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX daily_prices_date_index ON public.daily_prices USING btree (date);


--
-- Name: daily_prices daily_prices_stock_id_foreign; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.daily_prices
    ADD CONSTRAINT daily_prices_stock_id_foreign FOREIGN KEY (stock_id) REFERENCES public.stocks(id);


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
INSERT INTO public.migrations VALUES ('2021_05_09_035031_create_daily_prices_table', 2);


--
-- PostgreSQL database dump complete
--

