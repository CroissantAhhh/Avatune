import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';

import { loadUserByHash, addUserFollows } from '../../store/users';
import { loadUserPlaylists } from '../../store/playlists';
import { loadUserTracksMost } from '../../store/tracks';

import TrackContainer from '../../components/TrackContainer';

export default function UserPage() {
    const { userHash } = useParams();
    const [isLoaded, setIsLoaded] = useState(false);
    const dispatch = useDispatch();

    useEffect(() => {
        (async() => {
            const userId = await dispatch(loadUserByHash(userHash));
            await dispatch(addUserFollows(userId));
            await dispatch(loadUserPlaylists(userId));
            await dispatch(loadUserTracksMost(userId));
            setIsLoaded(true);
        })();
    }, [dispatch, userHash])

    const mainUser = useSelector(state => Object.values(state.users).filter(user => "main" in user.categories));
    const userFollowers = useSelector(state => Object.values(state.users).filter(user => "follower" in user.categories));
    const userFollowed = useSelector(state => Object.values(state.users).filter(user => "following" in user.categories));
    const userPlayists = useSelector(state => Object.values(state.playlists));
    const userTracks = useSelector(state => Object.values(state.tracks));

    return (
        <div className="user-page-container">
            {isLoaded && (
                <div className="user-page">
                    <div className="user-info">
                        <div className="user-avatar">

                        </div>
                        <div className="user-detailed-info">

                        </div>
                    </div>
                    <div className="user-playlists">

                    </div>
                    <div className="user-tracks">
                        <TrackContainer tracks={userTracks} category="user" />
                    </div>
                    <div className="user-followers">

                    </div>
                    <div className="user-following">

                    </div>
                </div>
            )}
        </div>
    )
}
