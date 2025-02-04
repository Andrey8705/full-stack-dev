--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars (
    id integer NOT NULL,
    brand character varying(30) NOT NULL,
    model character varying(30) NOT NULL,
    year integer NOT NULL,
    price integer,
    status character varying(20)
);


ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cars_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cars_id_seq OWNER TO postgres;

--
-- Name: cars_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cars_id_seq OWNED BY public.cars.id;


--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    iin bigint,
    phone character varying(20),
    email character varying(100) NOT NULL,
    CONSTRAINT clients_iin_check CHECK (((iin >= 0) AND (iin <= '999999999999'::bigint)))
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clients_id_seq OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_id_seq OWNED BY public.clients.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    first_name character varying(30),
    last_name character varying(30),
    "position" character varying(30),
    hire_date date,
    employee_id integer
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales (
    id integer NOT NULL,
    car_id integer,
    client_id integer,
    sale_date date,
    amount integer,
    employee_id integer
);


ALTER TABLE public.sales OWNER TO postgres;

--
-- Name: sales_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sales_id_seq OWNER TO postgres;

--
-- Name: sales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;


--
-- Name: cars id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars ALTER COLUMN id SET DEFAULT nextval('public.cars_id_seq'::regclass);


--
-- Name: clients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Name: sales id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (id, brand, model, year, price, status) FROM stdin;
1	Lada	Vesta	2015	20000000	В наличии
5	Aston Martin	-	2000	25000000	В наличии
3	Tesla	X5	2025	400000000	Под заказ
2	BMW	X5	2020	200000000	В наличии
4	Mazda	RX300	2018	20000000	В наличии
8	BMW	X5	2024	45000000	под заказ
11	Toyota	Land Cruiser	2024	52000000	под заказ
10	Mercedes	E-Class	2024	42000000	В наличии
12	Hyundai	Santa Fe	2023	22500000	В наличии
7	Hyundai	Accent	2023	9800000	В наличии
9	Kia	K5	2023	15500000	В наличии
6	Toyota	Camry	2024	18500000	В наличии
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients (id, first_name, last_name, iin, phone, email) FROM stdin;
1	Antony	Vice	810315513018	77777777777	Antony@mail.com
5	Азамат	Сериков	940825300123	+77071234567	azamat@mail.kz
6	Динара	Алиева	880915400789	+77082345678	dinara@mail.kz
7	Бауыржан	Нурланов	910304500456	+77093456789	baur@mail.kz
4	Bruce	Beller	810115713018	22222222222	Brucemail.com
3	Jane	Carter	810115713018	11111111111	Jane@mail.com
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, first_name, last_name, "position", hire_date, employee_id) FROM stdin;
1	Antony	Viceman	Manager	2023-02-12	\N
2	Paula	Wise	Cleaner	2020-12-10	\N
3	Ерлан	Касымов	Менеджер продаж	2023-01-15	\N
4	Айгуль	Нурпеисова	Старший менеджер	2022-05-20	\N
\.


--
-- Data for Name: sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales (id, car_id, client_id, sale_date, amount, employee_id) FROM stdin;
2	5	1	2024-08-13	25000000	3
1	2	1	2024-06-23	10000000	4
7	1	1	2024-02-15	18500000	1
8	4	3	2024-02-20	15500000	4
\.


--
-- Name: cars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_id_seq', 12, true);


--
-- Name: clients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_id_seq', 7, true);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 6, true);


--
-- Name: sales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sales_id_seq', 8, true);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (id);


--
-- Name: clients clients_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_email_key UNIQUE (email);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: sales sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);


--
-- Name: sales fk_employee; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: sales sales_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.cars(id);


--
-- Name: sales sales_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- PostgreSQL database dump complete
--

