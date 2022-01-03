import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';

import LoadingPage from '../LoadingPage';
import GeneralListing from '../../components/GeneralListing';

import './MyCategoryPage.css';

export default function MyCategoryPage() {
    const sessionUser = useSelector(state => state.session.user);
    const myPlaylists = useSelector(state => Object.values(state.playlists));
    const { category } = useParams();
    const [userListings, setUserListings] = useState();
    const [listingCategory, setListingCategory] = useState("");
    const [titleFormat, setTitleFormat] = useState("");
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        (async() => {
            setIsLoaded(false);
            switch(category) {
                case 'media':
                    const responseMedia = await fetch(`/api/media/byUser/${sessionUser.id}`);
                    const myMedia = await responseMedia.json();
                    setUserListings(myMedia.media);
                    setListingCategory('Medium');
                    setTitleFormat('My Media');
                    break;
                case 'artists':
                    const responseArtists = await fetch(`/api/artists/byUser/${sessionUser.id}`);
                    const myArtists = await responseArtists.json();
                    setUserListings(myArtists.artists);
                    setListingCategory('Artist');
                    setTitleFormat('My Artists');
                    break;
                case 'albums':
                    const responseAlbums = await fetch(`/api/albums/byUser/${sessionUser.id}`);
                    const myAlbums = await responseAlbums.json();
                    setUserListings(myAlbums.albums);
                    setListingCategory('Album');
                    setTitleFormat('My Albums');
                    break;
                case 'playlists':
                    setUserListings(myPlaylists);
                    setListingCategory('Playlist');
                    setTitleFormat('My Playlists');
                    break;
                case 'followers':
                    const responseFollowers = await fetch(`/api/users/followers/${sessionUser.id}`);
                    const myFollowers = await responseFollowers.json();
                    setUserListings(myFollowers.users);
                    setListingCategory('User');
                    setTitleFormat('My Followers');
                    break;
                case 'following':
                    const responseFollowing = await fetch(`/api/users/following/${sessionUser.id}`);
                    const myFollowing = await responseFollowing.json();
                    setUserListings(myFollowing.users);
                    setListingCategory('User');
                    setTitleFormat('Following');
                    break;
            };
            setIsLoaded(true);
        })()
    }, [category])

    return (
        <div className="my-categories-container background">
            {isLoaded ? (
                <div className="my-categories-page page-load-transition">
                    <div className="my-categories-header">
                        <p className="categories-header">{titleFormat}</p>
                    </div>
                    <div className="category-listings">
                        {userListings.map(listing => (
                            <GeneralListing key={listing.hashedId} item={listing} category={listingCategory} />
                        ))}
                    </div>
                </div>
            ) : (
                <LoadingPage />
            )}
        </div>
    )
}
