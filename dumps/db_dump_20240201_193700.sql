--
-- PostgreSQL database dump
--

-- Dumped from database version 14.10 (Homebrew)
-- Dumped by pg_dump version 14.10 (Homebrew)

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
-- Name: auto_data; Type: TABLE; Schema: public; Owner: dmytrolebid
--

CREATE TABLE public.auto_data (
    id integer NOT NULL,
    url character varying(255),
    title character varying(255),
    price_usd integer,
    odometer integer,
    username character varying(255),
    phone_number character varying(20),
    image_url character varying(255),
    images_count integer,
    car_number character varying(20),
    vin character varying(20),
    datetime_found timestamp without time zone
);


ALTER TABLE public.auto_data OWNER TO dmytrolebid;

--
-- Name: auto_data_id_seq; Type: SEQUENCE; Schema: public; Owner: dmytrolebid
--

CREATE SEQUENCE public.auto_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auto_data_id_seq OWNER TO dmytrolebid;

--
-- Name: auto_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmytrolebid
--

ALTER SEQUENCE public.auto_data_id_seq OWNED BY public.auto_data.id;


--
-- Name: auto_data id; Type: DEFAULT; Schema: public; Owner: dmytrolebid
--

ALTER TABLE ONLY public.auto_data ALTER COLUMN id SET DEFAULT nextval('public.auto_data_id_seq'::regclass);


--
-- Data for Name: auto_data; Type: TABLE DATA; Schema: public; Owner: dmytrolebid
--

COPY public.auto_data (id, url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, vin, datetime_found) FROM stdin;
1	https://example.com	Car Title	10000	50000	John Doe	123-456-7890	https://example.com/image.jpg	3	ABC123	VIN123	2024-01-31 12:00:00
2	https://example.com	Car Title	10000	50000	John Doe	123-456-7890	https://example.com/image.jpg	3	ABC123	VIN123	2024-01-31 12:00:00
3	https://example.com	Car Title	10000	50000	John Doe	123-456-7890	https://example.com/image.jpg	3	ABC123	VIN123	2024-01-31 12:00:00
4	https://example.com	Car Title	10000	50000	John Doe	123-456-7890	https://example.com/image.jpg	3	ABC123	VIN123	2024-01-31 12:00:00
5	https://example.com	Car Title	10000	50000	John Doe	123-456-7890	https://example.com/image.jpg	3	ABC123	VIN123	2024-01-31 12:00:00
6	https://auto.ria.com/uk/auto_skoda_superb_scout_35777152.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
7	https://auto.ria.com/uk/auto_land_rover_range_rover_35972005.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
8	https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35903311.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
9	https://auto.ria.com/uk/auto_bmw_3_series_35970816.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
10	https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35883468.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
11	https://auto.ria.com/uk/auto_volkswagen_passat_alltrack_35682264.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
12	https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35883493.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
13	https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35348238.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
14	https://auto.ria.com/uk/auto_volkswagen_id_4_crozz_35852534.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
15	https://auto.ria.com/uk/auto_dodge_durango_35950595.html	\N	\N	\N	\N	\N	\N	\N	\N	\N	2024-01-31 23:26:04
\.


--
-- Name: auto_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmytrolebid
--

SELECT pg_catalog.setval('public.auto_data_id_seq', 15, true);


--
-- Name: auto_data auto_data_pkey; Type: CONSTRAINT; Schema: public; Owner: dmytrolebid
--

ALTER TABLE ONLY public.auto_data
    ADD CONSTRAINT auto_data_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

