import { useSelector, useDispatch } from 'react-redux';
import { useEffect, useState } from 'react';
import { useLocation, useHistory } from 'react-router-dom';

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
    const { nextLocation } = useBrowsingHistory();
    const dispatch = useDispatch();
    const history = useHistory();
    const sessionUser = useSelector(state => state.session.user)
    const [isLoaded, setIsLoaded] = useState(false)
    const [latestAlbum, setLatestAlbum] = useState();

    function featuredLink() {
        nextLocation('/medium/FzNUn00EOTyibV58b871');
        history.push('/medium/FzNUn00EOTyibV58b871');
    }

    function greeting() {
        const currentTime = new Date();
        const hours = currentTime.getHours();
        if (hours >=5 && hours < 12) {
            return 'Good morning';
        } else if (hours >= 12 && hours < 18) {
            return 'Good afternoon';
        } else if (hours >= 18 && hours < 22) {
            return 'Good evening';
        } else {
            return 'suh';
        }
    };

    useEffect(() => {
        (async () => {
            setIsLoaded(false);
            await dispatch(loadUserAlbums(sessionUser.id));
            const response = await fetch('/api/albums/latest');
            const album = await response.json();
            setLatestAlbum(album.album);
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
        <div className="home-page-container background">
            {isLoaded ? (
                <div className="home-page page-load-transition">
                    <div className="welcome-section">
                        <p className="welcome-text">{`${greeting()}, ${sessionUser.username}`}</p>
                    </div>
                    <div className="featured-section l-horizontal">
                        <div className="featured-info">
                            <p className="featured-header">Top Medium of 2021</p>
                            <p className="featured-medium">Haikyu!!</p>
                            <p className="featured-link hover-pointer link-hover" onClick={featuredLink}>Go to Medium Page →</p>
                        </div>
                        <img className="featured-image" src="https://res.cloudinary.com/dmtj0amo0/image/upload/v1640406875/haikyuimage_fubjww.jpg" width="500px" alt="haikyu visual" />
                    </div>
                    <div className="home-tracks">
                        <div className="home-tracks-heading">
                            <p className="home-tracks-heading-text">Recently Played Tracks</p>
                        </div>
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
