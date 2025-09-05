SELECT
    activities.user_uuid,
    users.display_name,
    users.handle,
    activities.message,
    activities.created_at
    activities.expires_at
FROM
    public.activities
INNER JOIN public.users ON users.entry_uuid = activities.user_uuid
WHERE
    activities.uuid = %(uuid)s

    