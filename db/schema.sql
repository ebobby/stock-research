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
-- Name: tickers; Type: TABLE; Schema: public; Owner: stocks
--

CREATE TABLE public.tickers (
    id integer NOT NULL,
    symbol text NOT NULL,
    name text NOT NULL,
    exchange character(1) NOT NULL,
    etf boolean NOT NULL,
    status character(1) NOT NULL,
    cqs text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.tickers OWNER TO stocks;

--
-- Name: tickers_id_seq; Type: SEQUENCE; Schema: public; Owner: stocks
--

CREATE SEQUENCE public.tickers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tickers_id_seq OWNER TO stocks;

--
-- Name: tickers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stocks
--

ALTER SEQUENCE public.tickers_id_seq OWNED BY public.tickers.id;


--
-- Name: tickers id; Type: DEFAULT; Schema: public; Owner: stocks
--

ALTER TABLE ONLY public.tickers ALTER COLUMN id SET DEFAULT nextval('public.tickers_id_seq'::regclass);


--
-- Name: tickers tickers_pkey; Type: CONSTRAINT; Schema: public; Owner: stocks
--

ALTER TABLE ONLY public.tickers
    ADD CONSTRAINT tickers_pkey PRIMARY KEY (id);


--
-- Name: idx_tickers_symbol; Type: INDEX; Schema: public; Owner: stocks
--

CREATE INDEX idx_tickers_symbol ON public.tickers USING btree (symbol);


--
-- PostgreSQL database dump complete
--

