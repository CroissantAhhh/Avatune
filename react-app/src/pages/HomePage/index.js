import { useSelector, useDispatch } from 'react-redux';
import { useEffect, useState } from 'react';

import { loadUserAlbums, getLatestAlbum } from '../../store/albums';
import { loadUserPlaylistsMost } from '../../store/playlists';
import { loadUserMediaMost } from '../../store/media';
import { loadUserArtists } from '../../store/artists';
import { loadUserTracksMost } from '../../store/tracks';
// Store dispatches/fetches needed:
// - Albums: one album, most recent in database, links to the album page, 5 of user's most listened to albums (defined by most listened to songs in album)
// - Playlists: 5 of user's (random?), "see all" links to all of user's playlist
// - Media: 5 of user's followed (random, most played), "see all" links to all of user's followed media
// - Artists: 5 of users's followed (random, most played), "see all" links to all of user's followed artists
// - Tracks: 5 of user's most recently listened to songs

export default function HomePage() {
    // Newly Released Album Section
    // Your Playlists
    // Followed Media
    // Followed Artists
    // Recently Listened to Albums
    // Recently Played Tracks

    const dispatch = useDispatch();
    const sessionUser = useSelector(state => state.session.user)
    const [isLoaded, setIsLoaded] = useState(false)

    useEffect(async () => {
        await dispatch(loadUserAlbums(sessionUser.id));
        await dispatch(getLatestAlbum());
        await dispatch(loadUserPlaylistsMost(sessionUser.id));
        await dispatch(loadUserMediaMost(sessionUser.id));
        await dispatch(loadUserArtists(sessionUser.id))
        await dispatch(loadUserTracksMost(sessionUser.id))
        setIsLoaded(true)
    }, [dispatch, sessionUser])

    return (
        <div>
            {isLoaded && (
                <p>Home Page</p>
            )}
        </div>
    )
}
