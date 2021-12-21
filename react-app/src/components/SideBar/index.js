import { useState } from 'react';
import { useSelector } from 'react-redux';
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
    const [playlistsTab, setPlaylistsTab] = useState(true);
    const myPlaylists = useSelector(state => Object.values(state.playlists));
    const sessionUser = useSelector(state => state.session.user);
    const ownPlaylists = myPlaylists.filter(playlist => playlist.userId === sessionUser.id);
    const followedPlaylists = myPlaylists.filter(playlist => playlist.userId !== sessionUser.id);
    return (
        <div className="side-bar container l-vertical">
            <div className="side-bar-upper container l-vertical">
                <div className="home-button">

                </div>
                <div className="your-media">

                </div>
                <div className="your-artists">

                </div>
                <div className="your-albums">

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
