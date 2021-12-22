import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useHistory, useLocation } from 'react-router-dom';
// Functionality:
// Top Section Links:
//  - Link to home page
//  - Followed Media
//  - Followed Artists
//  - Liked Albums

// Lower Section: ALL PLAYLIST STUFF
// Two tabs: User created playlists, followed playlists

import './SideBar.css';

export default function SideBar() {
    const history = useHistory();
    const location = useLocation();

    const [playlistsTab, setPlaylistsTab] = useState(true);
    const [currentURL, setCurrentURL] = useState(location.pathname)

    const myPlaylists = useSelector(state => Object.values(state.playlists));
    const sessionUser = useSelector(state => state.session.user);
    const ownPlaylists = myPlaylists.filter(playlist => playlist.userId === sessionUser.id);
    const followedPlaylists = myPlaylists.filter(playlist => playlist.userId !== sessionUser.id);

    useEffect(() => {
        setCurrentURL(location.pathname);
    }, [location.pathname])

    console.log(location.pathname)
    console.log(currentURL)

    return (
        <div className="side-bar l-vertical">
            <div className="side-bar-upper l-vertical">
                <div className="side-bar-placeholder"></div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/home") ? "grey" : "black" }}
                        onClick={() => history.push('/home')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                        </svg>
                        <p className="side-bar-nav-label font-normal">Home</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/my/media") ? "grey" : "black" }}
                        onClick={() => history.push('/my/media')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                        </svg>
                        <p className="side-bar-nav-label font-normal">Media</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/my/artists") ? "grey" : "black" }}
                        onClick={() => history.push('/my/artists')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        <p className="side-bar-nav-label font-normal">Artists</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/my/albums") ? "grey" : "black" }}
                        onClick={() => history.push('/my/albums')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                        <p className="side-bar-nav-label font-normal">Albums</p>
                    </div>
                </div>
            </div>
            <div className="side-bar-middle l-vertical">
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        onClick={() => history.push('/home')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="side-bar-nav-label font-normal">Create Playlist</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        onClick={() => history.push(`/playlist/${ownPlaylists[0].hashedId}`)}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                        </svg>
                        <p className="side-bar-nav-label font-normal">Your Songs</p>
                    </div>
                </div>
            </div>
            <div className="side-bar-divider"></div>
            <div className="side-bar-lower l-vertical">
                <div className="playlist-tab-toggle l-horizontal">
                    <div
                        className="playlist-tab l-horizontal hover-pointer"
                        onClick={() => setPlaylistsTab(true)}
                        style={{ backgroundColor: playlistsTab ? "grey" : "black" }}>
                        <p className="playlist-tab-title font-normal">Created</p>
                    </div>
                    <div
                        className="playlist-tab l-horizontal hover-pointer"
                        onClick={() => setPlaylistsTab(false)}
                        style={{ backgroundColor: playlistsTab ? "black" : "grey" }}>
                        <p className="playlist-tab-title font-normal">Followed</p>
                    </div>
                </div>
                <div className="playlist-container">
                    {playlistsTab ? (
                        ownPlaylists.slice(1).map(playlist => (
                            <div key={playlist.hashedId} className="playlist-listing-container hover-pointer">
                                <div className="playlist-listing" onClick={() => history.push(`/playlist/${playlist.hashedId}`)}>
                                    <p className="playlist-listing-title font-narrow">{playlist.title}</p>
                                </div>
                            </div>
                        ))
                    ) : (
                        followedPlaylists.map(playlist => (
                            <div key={playlist.hashedId} className="playlist-listing-container hover-pointer">
                                <div className="playlist-listing" onClick={() => history.push(`/playlist/${playlist.hashedId}`)}>
                                    <p className="playlist-listing-title font-narrow">{playlist.title}</p>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    )
}
