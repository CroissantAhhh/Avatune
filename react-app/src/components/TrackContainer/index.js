
import TrackListing from '../TrackListing';

import './TrackContainer.css';

export default function TrackContainer({ tracks, category }) {

    let middleHeaders;

    switch(category) {
        case 'playlist':
            middleHeaders = (
                <>
                    <div className="track-heading-album">
                        <p>ALBUM</p>
                    </div>
                    <div className="track-heading-date-added">
                        <p>DATE ADDED</p>
                    </div>
                </>
            );
            break;
        case 'album':
            middleHeaders = (
                <div className="track-heading-plays l-horizontal">
                    <p>PLAYS</p>
                </div>
            );
            break;
        case 'user':
            middleHeaders = (
                <div className="track-heading-album">
                    <p>ALBUM</p>
                </div>
            );
            break;
    };

    console.log(category)

    return (
        <div className="track-container">
            <div className="track-container-placeholder"></div>
            <div className="track-container-heading l-horizontal-spread">
                <div className="track-heading-index l-horizontal">
                    <p>#</p>
                </div>
                <div className="track-heading-image"></div>
                <div className="track-heading-title">
                    <p>TITLE</p>
                </div>
                <div className="track-heading-middle l-horizontal-spread">
                    {middleHeaders}
                </div>
                <div className="track-heading-duration l-horizontal">
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
            </div>
            <div className="track-container-divider"></div>
            <div className="track-container-content">
                {tracks.map((track, index) => (
                    <TrackListing key={track.id} track={track} index={index + 1} category={category}/>
                ))}
            </div>
        </div>
    )
}
