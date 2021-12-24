import { useSelector } from 'react-redux';
import { useState, useEffect } from 'react';

import './TrackListing.css';


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

    function durationFormat(duration) {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        return `${minutes}:${seconds}`;
    }

    return (
        <div className="track-listing l-horizontal-spread hover-pointer">
            <div className="track-index track-category l-horizontal">
                <p>{index}</p>
            </div>
            <div className="track-image track-category l-horizontal">
                <img src={track.image} alt="track artwork" height="40px" width="40px" />
            </div>
            <div className="track-title track-category">
                <p className="track-title-text font-normal">{track.title}</p>
                <p className="track-artists-text">{track.artists.join(", ")}</p>
            </div>
            <div className="track-middle-section l-horizontal-spread track-category">
                {playlist ? (
                    <>
                        <div className="track-album track-category">
                            <p className="track-album-title track-category">{track.album}</p>
                        </div>
                        <div className="track-date-added">
                            <p>{timeElapsed(track.dateAdded)}</p>
                        </div>
                    </>
                ) : (
                    <div className="track-plays track-category l-horizontal">
                        <p>{track.plays}</p>
                    </div>
                )}
            </div>

            <div className="track-favorite track-category l-horizontal">
                {isLiked ? (
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                )}
            </div>
            <div className="track-duration track-category l-horizontal">
                <p>{durationFormat(track.duration)}</p>
            </div>
        </div>
    )
}
