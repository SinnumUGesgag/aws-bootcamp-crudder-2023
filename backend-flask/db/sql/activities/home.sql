SELECT
    activities.user_uuid,
    users.display_name,
    users.handle,
    activities.message,
    activities.replies_count,
    activities.reposts_count,
    activities.likes_count,
    activities.reply_to_activity_uuid,
    activities.expires_at,
    activities.created_at
FROM
    public.activities
INNER JOIN public.users ON users.entry_uuid = activities.user_uuid
ORDER BY activities.created_at DESC