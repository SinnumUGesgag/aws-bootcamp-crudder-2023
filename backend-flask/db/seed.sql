
INSERT INTO public.users (user_uuid, display_name, handle, email, cognito_user_id, created_at)
VALUES (uuid_generate_v4(), "Mock User", "mockuser", "mockUser@mock.com", "Mock", current_timestamp);

/* 
User Schema is set to require the followering per entry: 
{
user_uuid (UUID),
display_name (text),
handle (text),
email (text),
cognito_user_id (text),
created_at T(current_timestamp)
}
*/

INSERT INTO public.activities (user_uuid, message, expires_at, created_at)
VALUES
	(
		(SELECT uuid from public.users WHERE users.handle = 'mockuser' LIMIT 1),
		'Imported as Test Seed Data!',
		current_timestamp + interval '10 day',
		current_timestamp
	);

/*
Activities' Schema is set to require the followering per entry: 
{
user_uuid (generated per user),	
message (text),
created_at (current_timestamp)
*/