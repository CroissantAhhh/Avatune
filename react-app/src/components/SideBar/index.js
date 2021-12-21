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


export default function SideBar() {
    const [playlistsTab, setPlaylistsTab] = useState(true);
    const myPlaylists = useSelector(state => Object.values(state.playlists));
    const
    return (
        <div className="side-bar container">
            <div className="side-bar-upper container">
                <div className="home-button">

                </div>
                <div className="your-media">

                </div>
                <div className="your-artists">

                </div>
                <div className="your-albums">

                </div>
            </div>
            <div className="side-bar-lower container">

            </div>
        </div>
    )
}
