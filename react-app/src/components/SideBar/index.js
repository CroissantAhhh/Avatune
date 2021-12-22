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
                        <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                        </svg>
                        <p className="side-bar-nav-label">Home</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/my/media") ? "grey" : "black" }}
                        onClick={() => history.push('/my/media')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
                        </svg>
                        <p className="side-bar-nav-label">Media</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/my/artists") ? "grey" : "black" }}
                        onClick={() => history.push('/my/artists')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                        </svg>
                        <p className="side-bar-nav-label">Artists</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        style={{ backgroundColor: currentURL.includes("/my/albums") ? "grey" : "black" }}
                        onClick={() => history.push('/my/albums')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
                        </svg>
                        <p className="side-bar-nav-label">Albums</p>
                    </div>
                </div>
            </div>
            <div className="side-bar-divider"></div>
            <div className="side-bar-middle l-vertical">
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        onClick={() => history.push('/home')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
                        </svg>
                        <p className="side-bar-nav-label">Create Playlist</p>
                    </div>
                </div>
                <div className="side-bar-nav l-horizontal hover-pointer">
                    <div
                        className="side-bar-nav-content l-horizontal"
                        onClick={() => history.push('/home')}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
                        </svg>
                        <p className="side-bar-nav-label">Your Songs</p>
                    </div>
                </div>
            </div>
            <div className="side-bar-lower container l-vertical">
                <div className="your-playlists">
                    <p>Playlists</p>
                </div>
                <div className="playlist-tab-toggle l-horizontal">
                    <div className="own-playlists" onClick={() => setPlaylistsTab(true)}>
                        <p>My Playlists</p>
                    </div>
                    <div className="followed-playlists" onClick={() => setPlaylistsTab(false)}>
                        <p>Followed Playlists</p>
                    </div>
                </div>
                <div className="playlist-container">
                    {playlistsTab ? (
                        ownPlaylists.map(playlist => (
                            <div className="playlist-listing">
                                {playlist.title}
                            </div>
                        ))
                    ) : (
                        followedPlaylists.map(playlist => (
                            <div className="playlist-listing">
                                {playlist.title}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    )
}
