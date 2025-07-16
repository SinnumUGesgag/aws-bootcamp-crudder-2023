INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES	 ("Mock User", "mockuser", "Mock");

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
	(
		(SELECT uuid from public.users WHERE users.handle = 'mockuser' LIMIT 1),
		'Imported as Test Seed Data!',
		current_timestamp + interval '10 day'
	);