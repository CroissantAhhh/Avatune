import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';

import { loadAlbumByHash } from '../../store/albums';
import { loadAlbumTracks } from '../../store/tracks';

import LoadingPage from '../LoadingPage';
import TrackContainer from '../../components/TrackContainer';
import GeneralListingContainer from '../../components/GeneralListingContainer';

import './AlbumPage.css';

export default function AlbumPage() {
    const [isLoaded, setIsLoaded] = useState(false);
    const dispatch = useDispatch();
    const { albumHash } = useParams();
    const [mediumAlbums, setMediumAlbums] = useState();
    const [artistAlbums, setArtistAlbums] = useState();

    useEffect(() => {
        (async() => {
            setIsLoaded(false);
            const currentAlbum = await dispatch(loadAlbumByHash(albumHash))
            await dispatch(loadAlbumTracks(currentAlbum.id));
            const fetch1 = await fetch(`/api/albums/byMedia/${currentAlbum.medium.id}`);
            const response1 = await fetch1.json();
            setMediumAlbums(response1.albums);
            const fetch2 = await fetch(`/api/albums/byArtist/${currentAlbum.artists[0].id}`);
            const response2 = await fetch2.json();
            setArtistAlbums(response2.albums);
            setIsLoaded(true);
        })()
    }, [dispatch, albumHash])
    // Album information section

    // Album tracks

    // More by the main artist (the first one)
    const album = useSelector(state => Object.values(state.albums))[0];
    const albumTracks = useSelector(state => Object.values(state.tracks));

    return (
        <div className="album-page-container background">
            {isLoaded ? (
                <div className="album-page page-load-transition">
                    <div className="album-header">

                    </div>
                    <TrackContainer tracks={albumTracks} category='album' />
                    <div className="album-more-from-medium">
                        <GeneralListingContainer title={`More from ${album.medium.title}`} listings={mediumAlbums} category="Album" />
                    </div>
                    <div className="album-more-from-artist">
                        <GeneralListingContainer title={`More by ${album.artists[0].title}`} listings={artistAlbums} category="Album" />
                    </div>
                </div>
            ) : (
                <LoadingPage />
            )}
        </div>
    )
}
