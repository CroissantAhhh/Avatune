import { useSelector, useDispatch } from 'react-redux';
import { useEffect, useState } from 'react';

import { loadUserAlbums, getLatestAlbum } from '../../store/albums';
import { loadUserMediaMost } from '../../store/media';
import { loadUserArtists } from '../../store/artists';
import { loadUserTracksMost } from '../../store/tracks';

import { useBrowsingHistory } from '../../context/BrowsingHistoryContext';

import GeneralListing from '../../components/GeneralListing';
import GeneralListingContainer from '../../components/GeneralListingContainer';
import TrackContainer from '../../components/TrackContainer';
import TrackListing from '../../components/TrackListing';

import LoadingPage from '../LoadingPage';

import './HomePage.css'
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
    const { locations, setLocation } = useBrowsingHistory();
    const dispatch = useDispatch();
    const sessionUser = useSelector(state => state.session.user)
    const [isLoaded, setIsLoaded] = useState(false)

    useEffect(() => {
        (async () => {
            setIsLoaded(false);
            await dispatch(loadUserAlbums(sessionUser.id));
            await dispatch(getLatestAlbum());
            await dispatch(loadUserMediaMost(sessionUser.id));
            await dispatch(loadUserArtists(sessionUser.id))
            await dispatch(loadUserTracksMost(sessionUser.id))
            setIsLoaded(true)
        })();
    }, [dispatch, sessionUser])

    const albums = useSelector(state => Object.values(state.albums));
    const artists = useSelector(state => Object.values(state.artists));
    const media = useSelector(state => Object.values(state.media));
    const playlists = useSelector(state => Object.values(state.playlists));
    const tracks = useSelector(state => Object.values(state.tracks))

    return (
        <div className="home-page-container">
            {isLoaded ? (
                <div>
                    <div className="tracks">
                        <TrackContainer tracks={tracks} category={"album"} />
                    </div>
                    <div className="listings-section">
                        <GeneralListingContainer title="Your Albums" listings={albums} category="Album" />
                    </div>
                    <div className="listings-section">
                        <GeneralListingContainer title="Your Artists" listings={artists} category="Artist" />
                    </div>
                    <div className="listings-section">
                        <GeneralListingContainer title="Your Media" listings={media} category="Medium" />
                    </div>
                    <div className="listings-section">
                        <GeneralListingContainer title="Your Playlists" listings={playlists} category="Playlist" />
                    </div>
                </div>
            ) : (
                <LoadingPage />
            )}
        </div>
    )
}
