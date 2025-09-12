
INSERT INTO public.users (display_name, handle, email, cognito_user_id) 
VALUES
	('Primer User', 'primeruser', 'primeruser@mock.com', 'MockA'),
	('Mock User', 'mockuser', 'mockUser@mock.com', 'MockB'),
	('Andrew Brown', 'andrewbrown', 'andrewbrown@mock.com', 'MockC'),
	('TestUser', 'Test_User','mich.shrader@gmail.com', 'e17b95c0-3021-7086-750b-c8644071bfe5');



INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
	(
		(SELECT entry_uuid from public.users WHERE users.handle = 'mockuser' LIMIT 1),
		'Imported as Test Seed Data!',
		current_timestamp + interval '10 day'
	);

