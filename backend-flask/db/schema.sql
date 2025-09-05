
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;

CREATE TABLE public.users (
	entry_uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	display_name text NOT NULL,
	handle text NOT NULL,
	email text NOT NULL,
	cognito_user_id text NOT NULL,
	created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities (
	entry_uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
	user_uuid UUID NOT NULL,
	message text NOT NULL,
	replies_count integer DEFAULT 0,
	reposts_count integer DEFAULT 0,
	likes_count integer DEFAULT 0,
	reply_to_activity_uuid integer,
	expires_at TIMESTAMP,
	created_at TIMESTAMP default current_timestamp NOT NULL
);
