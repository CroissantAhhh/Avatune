import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { loadPlaylistTracks } from '../../store/tracks';

import TrackContainer from '../../components/TrackContainer';
import TrackListing from '../../components/TrackListing';

import './PlaylistPage.css';

export default function PlaylistPage() {
    const dispatch = useDispatch();
    const { playlistHash } = useParams();
    const [isLoaded, setIsLoaded] = useState(false);
    const playlists = useSelector(state => Object.values(state.playlists))
    const currentPlaylist = playlists?.find(playlist => playlist.hashedId === playlistHash)

    useEffect(() => {
        (async () => {
            setIsLoaded(false);
            await dispatch(loadPlaylistTracks(currentPlaylist?.id));
            setIsLoaded(true);
        })();
    }, [playlistHash])
    // Playlist information + edit/delete controls
    // Tracklist

    const tracks = useSelector(state => Object.values(state.tracks))

    function totalDuration() {
        const totalSeconds = tracks.reduce((prev, curr) => prev + curr.duration, 0);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes =  Math.floor((totalSeconds - hours * 3600) / 60);
        const seconds = totalSeconds % 60;
        const hoursStr = hours > 0 ? `${hours} hours ` : '';
        const minutesStr = `${minutes} minutes `;
        const secondsStr = seconds > 0 ? `${seconds} seconds` : '';
        return hoursStr + minutesStr + secondsStr;
    };

    return (
        <div className="playlist-page-container background">
            {isLoaded && (
                <div className="playlist-page page-load-transition">
                    <div className="playlist-header l-horizontal">
                        <div className="playlist-image-section l-horizontal">
                            <img className="playlist-image shadowed rounded" src={currentPlaylist.image} height="250px" alt="playlist image" />
                        </div>
                        <div className="playlist-detailed-info">
                            <p className="playlist-heading">Playlist</p>
                            <p className="playlist-title">{currentPlaylist.title}</p>
                            <div className="user-info-numbers">
                                <p className="num-playlists">{`${currentPlaylist.owner.name}`}</p>
                                <p className="album-songs-info">{`${tracks.length} songs`}</p>
                            </div>
                        </div>
                    </div>
                    <TrackContainer tracks={tracks} category={"playlist"} />
                </div>
            )}
        </div>
    )
}
