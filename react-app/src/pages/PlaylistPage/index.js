import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { loadPlaylistTracks } from '../../store/tracks';

import TrackContainer from '../../components/TrackContainer';
import TrackListing from '../../components/TrackListing';

export default function PlaylistPage() {
    const dispatch = useDispatch();
    const { playlistHash } = useParams();
    const [isLoaded, setIsLoaded] = useState(false);
    const playlists = useSelector(state => Object.values(state.playlists))
    const currentPlaylist = playlists?.find(playlist => playlist.hashedId === playlistHash)

    useEffect(() => {
        (async () => {
            await dispatch(loadPlaylistTracks(currentPlaylist?.id));
            await setIsLoaded(true);
        })();
    }, [playlistHash])
    // Playlist information + edit/delete controls
    // Tracklist

    const tracks = useSelector(state => Object.values(state.tracks))

    return (
        <div>
            {isLoaded && (
                <div>
                    <TrackContainer tracks={tracks} playlist={true} />
                </div>
            )}
        </div>
    )
}
