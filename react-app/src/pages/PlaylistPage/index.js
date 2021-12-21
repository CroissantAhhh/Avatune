import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { loadPlaylistByHash } from '../../store/playlists';
import { loadPlaylistTracks } from '../../store/tracks';

import TrackListing from '../../components/TrackListing';

export default function PlaylistPage() {
    const dispatch = useDispatch();
    const { playlistHash } = useParams();
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        (async () => {
            const playlistId = await dispatch(loadPlaylistByHash(playlistHash));
            await dispatch(loadPlaylistTracks(playlistId));
            setIsLoaded(true);
        })();
    }, [])
    // Playlist information + edit/delete controls
    // Tracklist

    const playlist = useSelector(state => Object.values(state.playlists)[0])
    const tracks = useSelector(state => Object.values(state.tracks))

    return (
        <div>
            {isLoaded && (
                <div>
                    {tracks.map((track, index) => (
                        <TrackListing key={track.id} track={track} index={index + 1} playlist={true} />
                    ))}
                </div>
            )}
        </div>
    )
}
