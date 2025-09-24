Run SQL
SELECT users.uuid
FROM public.users
WHERE uesrs.cognito_user_id = %(cognito_user_id)s
LIMiT 1