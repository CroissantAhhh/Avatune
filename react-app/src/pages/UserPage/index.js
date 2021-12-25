import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';

import { loadUserByHash, addUserFollows } from '../../store/users';
import { loadUserPlaylists } from '../../store/playlists';
import { loadUserTracksMost } from '../../store/tracks';

import TrackContainer from '../../components/TrackContainer';
import GeneralListingContainer from '../../components/GeneralListingContainer';

import LoadingPage from '../LoadingPage';

import './UserPage.css';

export default function UserPage() {
    const { userHash } = useParams();
    const [isLoaded, setIsLoaded] = useState(false);
    const [userPlaylists, setUserPlaylists] = useState([]);
    const dispatch = useDispatch();

    useEffect(() => {
        (async() => {
            setIsLoaded(false);
            const userId = await dispatch(loadUserByHash(userHash));
            await dispatch(addUserFollows(userId));
            // await dispatch(loadUserPlaylists(userId));
            const response = await fetch(`/api/playlists/byUser/${userId}`);
            const playlists = await response.json();
            setUserPlaylists(playlists.playlists)
            await dispatch(loadUserTracksMost(userId));
            setIsLoaded(true);
        })();
    }, [dispatch, userHash])

    const mainUser = useSelector(state => Object.values(state.users).filter(user => user.categories.includes("main"))[0]);
    const userFollowers = useSelector(state => Object.values(state.users).filter(user => user.categories.includes("follower")));
    const userFollowed = useSelector(state => Object.values(state.users).filter(user => user.categories.includes("following")));
    // const userPlaylists = useSelector(state => Object.values(state.playlists));
    const userTracks = useSelector(state => Object.values(state.tracks));

    return (
        <div className="user-page-container background">
            {isLoaded ? (
                <div className="user-page page-load-transition">
                    <div className="user-info l-horizontal">
                        <div className="user-avatar l-horizontal">
                            <img className="avatar-image shadowed rounded" src={mainUser.image} height="250px" alt="user avatar" />
                        </div>
                        <div className="user-detailed-info">
                            <p className="profile-heading">Profile</p>
                            <p className="user-username">{mainUser.username}</p>
                            <div className="user-info-numbers">
                                <p className="num-playlists">{`${userPlaylists.length} Playlists · `}</p>
                                <p className="num-followers">{`${userFollowers.length} Followers · `}</p>
                                <p className="num-followed">{`${userFollowed.length} Following`}</p>
                            </div>
                        </div>
                    </div>
                    <div className="user-tracks">
                        <div className="user-tracks-heading">
                            <p className="user-tracks-heading-text">Favorite Tracks</p>
                        </div>
                        <TrackContainer tracks={userTracks} category="user" />
                    </div>
                    <div className="user-playlists">
                        <GeneralListingContainer title="Playlists" listings={userPlaylists} category="Playlist" />
                    </div>
                    <div className="user-followers">
                        <GeneralListingContainer title="Followers" listings={userFollowers} category="User" />
                    </div>
                    <div className="user-following">
                        <GeneralListingContainer title="Following" listings={userFollowed} category="User" />
                    </div>
                </div>
            ) : (
                <LoadingPage />
            )}
        </div>
    )
}
