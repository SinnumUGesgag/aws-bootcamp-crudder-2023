import './ProfileHeading.css';

import EditProfileButton from '../components/EditProfileButton';

export default function ProfileHeading(props) {
    const backgroundImage = 'url("https://{ASSETS_BUCKET_NAME}/banners/bannerSpace.jpg")';
    const styles = {
        backgroundImage: backgroundImage,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
    };

    if (!props.profile) {
        return <div>Loading profile...</div>; // Or return null, or a specific "Not Found" message
    }

    return (
        <div className='activity_feed_heading profile_heading'>
            <div className='title'>{props.profile.display_name}</div>
            <div class="cruds_count">{props.profile.cruds_count} Cruds</div>
            <div class="banner" style={styles} >
                <div className="avatar">
                    <img src="https://{ASSETS_BUCKET_NAME}/data.jpg"></img>
                </div>
            </div>
            <div class="info">
                <div class='id'></div>
                    <div className='display_name'>{props.profile.display_name}</div>
                    <div className="handle">@{props.profile.handle}</div>
            </div>
            <EditProfileButton setPopped={props.setPopped} />
        </div>
    );
}



