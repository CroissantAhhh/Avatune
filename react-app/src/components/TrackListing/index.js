import { useSelector } from 'react-redux';
import { useState, useEffect } from 'react';


export default function TrackListing({ track, index, playlist }) {
    const likedSongs = useSelector(state => Object.values(state.playlists)[0].trackIds)
    const [isLiked, setIsLiked] = useState(likedSongs.includes(track.id));

    useEffect(() => {
        setIsLiked(likedSongs.includes(track.id));
    }, [likedSongs]);

    function timeElapsed(seconds) {
        if (seconds < 60) {
            return `${seconds} seconds ago`;
        } else if (seconds < 3600) {
            return `${Math.floor(seconds / 60)} minutes ago`
        } else if (seconds < 86400) {
            return `${Math.floor(seconds / 3600)} hours ago`
        } else if (seconds < 2592000) {
            return `${Math.floor(seconds / 86400)} days ago`
        } else {
            const dateInSeconds = Math.floor(Date.now() / 1000) - seconds;
            const originalDate = new Date(dateInSeconds * 1000);
            let dateString = originalDate.toDateString();
            const dateComponents = dateString.split(" ");
            return `${dateComponents[1]} ${dateComponents[2]}, ${dateComponents[3]}`;
        }
    }

    return (
        <div className="track-listing">
            <div className="track-index">
                <p>{index}</p>
            </div>
            <div className="track-image">
                <img src={track.image} alt="track artwork" height="100px" width="100px" />
            </div>
            <div className="track-title">
                <p>{track.title}</p>
                {playlist && (
                    <p>{track.artists.join(", ")}</p>
                )}
            </div>
            <div className="track-middle-section">
                {playlist ? (
                    <>
                        <div className="track-album">
                            <p>{track.album}</p>
                        </div>
                        <div className="track-date-added">
                            <p>{timeElapsed(track.dateAdded)}</p>
                        </div>
                    </>
                ) : (
                    <div className="track-plays">
                        <p>{track.plays}</p>
                    </div>
                )}
            </div>

            <div className="track-favorite">
                {isLiked ? (
                    <p>HEART</p>
                ) : (
                    <p>NO HEART</p>
                )}
            </div>
            <div className="track-duration">
                <p>{track.duration}</p>
            </div>
        </div>
    )
}
