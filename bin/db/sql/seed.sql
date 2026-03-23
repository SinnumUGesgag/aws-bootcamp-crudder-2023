
INSERT INTO public.users (display_name, handle, email, cognito_user_id) 
VALUES
	('Primer User', 'primeruser', 'primeruser@mock.com', 'MockPrime'),
	('Mock User', 'mockuser', 'mockUser@mock.com', 'MockU'),
	('Andrew Brown', 'andrewbrown', 'andrewbrown@mock.com', 'MockAndrew'),
	('TestUser', 'Test_User','mich.shrader@gmail.com', 'e1eb7570-2081-70ab-bbca-73fd3a6430c5');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
	(
		(SELECT entry_uuid from public.users WHERE users.handle = 'mockuser' LIMIT 1),
		'Imported as Test Seed Data!',
		current_timestamp + interval '10 day'
	);

