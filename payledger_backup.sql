--
-- PostgreSQL database dump
--

\restrict BVFyk6ZecsNbw5cRx23mUYf2yAt7p1PPI8LUhYFYOCxBXWt1TY1sJ9Q2yn85mr4

-- Dumped from database version 15.19 (Homebrew)
-- Dumped by pg_dump version 15.19 (Homebrew)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: ledger_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ledger_entries (
    id integer NOT NULL,
    transaction_id integer NOT NULL,
    wallet_id integer,
    entry_type character varying(10) NOT NULL,
    amount numeric(15,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    account_type character varying(20) NOT NULL
);


--
-- Name: ledger_entries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ledger_entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ledger_entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ledger_entries_id_seq OWNED BY public.ledger_entries.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    reference character varying(50) NOT NULL,
    transaction_type character varying(30) NOT NULL,
    amount numeric(15,2) NOT NULL,
    status character varying(20) NOT NULL,
    initiated_by integer NOT NULL,
    remark character varying(255),
    idempotency_key character varying(100),
    created_at timestamp without time zone NOT NULL
);


--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    verification_status character varying(20) NOT NULL,
    created_at timestamp without time zone
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: wallets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.wallets (
    id integer NOT NULL,
    wallet_number character varying(20) NOT NULL,
    user_id integer NOT NULL,
    balance numeric(15,2) NOT NULL,
    status character varying(20) NOT NULL
);


--
-- Name: wallets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.wallets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: wallets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.wallets_id_seq OWNED BY public.wallets.id;


--
-- Name: ledger_entries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ledger_entries ALTER COLUMN id SET DEFAULT nextval('public.ledger_entries_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: wallets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets ALTER COLUMN id SET DEFAULT nextval('public.wallets_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
c8d17b626a85
\.


--
-- Data for Name: ledger_entries; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ledger_entries (id, transaction_id, wallet_id, entry_type, amount, created_at, account_type) FROM stdin;
1	1	\N	DEBIT	100.00	2026-08-17 11:32:13.75555	SYSTEM
2	1	1	CREDIT	100.00	2026-08-17 11:32:13.75556	WALLET
3	2	1	DEBIT	30.00	2026-08-17 11:36:25.262083	WALLET
4	2	\N	CREDIT	30.00	2026-08-17 11:36:25.262087	SYSTEM
5	3	\N	DEBIT	500.00	2026-08-17 14:58:18.718821	SYSTEM
6	3	2	CREDIT	500.00	2026-08-17 14:58:18.71883	WALLET
7	5	2	DEBIT	100.00	2026-08-17 15:08:15.262256	WALLET
8	5	1	CREDIT	100.00	2026-08-17 15:08:15.262264	WALLET
9	6	\N	DEBIT	500.00	2026-08-17 18:49:46.674086	SYSTEM
10	6	6	CREDIT	500.00	2026-08-17 18:49:46.674102	WALLET
11	7	6	DEBIT	100.00	2026-08-17 18:51:42.371884	WALLET
12	7	\N	CREDIT	100.00	2026-08-17 18:51:42.371888	SYSTEM
13	8	6	DEBIT	100.00	2026-08-17 19:03:04.196489	WALLET
14	8	4	CREDIT	100.00	2026-08-17 19:03:04.196497	WALLET
15	9	4	DEBIT	10.00	2026-08-17 19:13:54.694512	WALLET
16	9	5	CREDIT	10.00	2026-08-17 19:13:54.694522	WALLET
17	10	4	DEBIT	10.00	2026-08-17 19:16:58.919407	WALLET
18	10	5	CREDIT	10.00	2026-08-17 19:16:58.919412	WALLET
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.transactions (id, reference, transaction_type, amount, status, initiated_by, remark, idempotency_key, created_at) FROM stdin;
1	TXN-90F02846763F	ADMIN_CREDIT	100.00	COMPLETED	1	Initial wallet credit	\N	2026-08-17 11:32:13.746608
2	TXN-5120AC8F47FB	ADMIN_DEBIT	30.00	COMPLETED	1	Test debit	\N	2026-08-17 11:36:25.260855
3	TXN-78CD865BAC78	ADMIN_CREDIT	500.00	COMPLETED	1	Initial transfer test	\N	2026-08-17 14:58:18.708769
5	TXN-BC770F2F94DF	MEMBER_TRANSFER	100.00	COMPLETED	4	Test transfer	\N	2026-08-17 15:08:15.257796
6	TXN-4B0FBFE8E1E7	ADMIN_CREDIT	500.00	COMPLETED	1	Wallet credit test	\N	2026-08-17 18:49:46.664055
7	TXN-FAC8AEED2210	ADMIN_DEBIT	100.00	COMPLETED	1	Wallet debit test	\N	2026-08-17 18:51:42.369565
8	TXN-A39DCB215C10	MEMBER_TRANSFER	100.00	COMPLETED	5	Test transfer to Alice	\N	2026-08-17 19:03:04.191767
9	TXN-61C90D6B44B7	MEMBER_TRANSFER	10.00	COMPLETED	2	Duplicate transfer test	\N	2026-08-17 19:13:54.687977
10	TXN-F33766C368E9	MEMBER_TRANSFER	10.00	COMPLETED	2	Duplicate transfer test	\N	2026-08-17 19:16:58.918055
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, name, email, password_hash, role, verification_status, created_at) FROM stdin;
1	Admin	nikithats23@gmail.com	scrypt:32768:8:1$RQP6rMElhqCwhnzq$dbc03123fefd225c1d594af87288c8fd3f9284fc18890c203b15ce50d14fbe4812bc0482c9a07b4298e55e68940fd7544581639f74a73808f7c10b53ca0f3928	ADMIN	VERIFIED	2026-08-16 12:44:40.296997
4	Charlie	hi123@gmail.com	scrypt:32768:8:1$F8h8bkGQokRc5zaW$bdfe133a4cd0fa02c02b1245f0b09bc2ee409d2f877f811d8b95b8184431bf1ca776cdbd2ac10d7d850ee85a80dad7bc12969d08d761b75b4197881c9d9c2385	MEMBER	VERIFIED	2026-08-16 14:10:01.489073
2	Alice	srinivasreddynikitha@gmail.com	scrypt:32768:8:1$ecMs04jplgOql8iD$3e8d171c15509da6a69316052f0c950556b3998ad1bdedff006c1d467d77afa228e39063c77efc5de8b9bea5656ae8079e5942dad8a1ea1ea44d6bed58a84426	MEMBER	VERIFIED	2026-08-16 13:36:01.389514
5	Test Member	payledger.test2026@gmail.com	scrypt:32768:8:1$MBcRJAKJsNHS1YDG$a604773d28c2d7e41193fde18c9bcef39c33a2d428e7346e288f2739e4d0018dc375d26fb8953ba8b905903fc13f79bf83b0063c3d58d6c41ac0b4170461c2ca	MEMBER	VERIFIED	2026-08-17 17:25:58.580844
3	Bob	nikitha56@gmail.com	scrypt:32768:8:1$jkxc3F4o65PRoFtD$ebf353e9a163b34b0ab84ffc8b4b5bb0bc7d81509ad03a3b352745f3f648c287e53552a3804c4c92440e5dd572a999d87ca3bfd996f83d5afc2526433e6a28eb	MEMBER	VERIFIED	2026-08-16 14:05:36.835248
\.


--
-- Data for Name: wallets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.wallets (id, wallet_number, user_id, balance, status) FROM stdin;
1	PL00000001	1	170.00	ACTIVE
2	PL00000002	4	400.00	ACTIVE
6	PL00000006	5	300.00	ACTIVE
4	PL00000003	2	80.00	ACTIVE
5	PL00000005	3	20.00	ACTIVE
\.


--
-- Name: ledger_entries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ledger_entries_id_seq', 18, true);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.transactions_id_seq', 10, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: wallets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.wallets_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: ledger_entries ledger_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ledger_entries
    ADD CONSTRAINT ledger_entries_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_idempotency_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_idempotency_key_key UNIQUE (idempotency_key);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_reference_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_reference_key UNIQUE (reference);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_key UNIQUE (user_id);


--
-- Name: wallets wallets_wallet_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_wallet_number_key UNIQUE (wallet_number);


--
-- Name: ledger_entries ledger_entries_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ledger_entries
    ADD CONSTRAINT ledger_entries_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES public.transactions(id);


--
-- Name: ledger_entries ledger_entries_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ledger_entries
    ADD CONSTRAINT ledger_entries_wallet_id_fkey FOREIGN KEY (wallet_id) REFERENCES public.wallets(id);


--
-- Name: transactions transactions_initiated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_initiated_by_fkey FOREIGN KEY (initiated_by) REFERENCES public.users(id);


--
-- Name: wallets wallets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict BVFyk6ZecsNbw5cRx23mUYf2yAt7p1PPI8LUhYFYOCxBXWt1TY1sJ9Q2yn85mr4

