import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';

import { loadArtistByHash } from '../../store/artists';
import { loadArtistTracksMost } from '../../store/tracks';

import TrackContainer from '../../components/TrackContainer';
import GeneralListingContainer from '../../components/GeneralListingContainer';

import LoadingPage from '../LoadingPage';

import './ArtistPage.css';

export default function ArtistPage() {
    const dispatch = useDispatch();
    const [isLoaded, setIsLoaded] = useState(false);
    const { artistHash } = useParams();
    const [artistAlbums, setArtistAlbums] = useState();

    useEffect(() => {
        (async() => {
            setIsLoaded(false);
            const artistId = await dispatch(loadArtistByHash(artistHash));
            await dispatch(loadArtistTracksMost(artistId));
            const response2 = await fetch(`/api/albums/byArtist/${artistId}`);
            const albums = await response2.json();
            setArtistAlbums(albums.albums);
            setIsLoaded(true);
        })();
    }, [dispatch, artistHash]);

    const currentArtist = useSelector(state => Object.values(state.artists))[0];
    const artistTracks = useSelector(state => Object.values(state.tracks));
    // Artist information

    // Most played tracks section

    // Albums section

    return (
        <div className="artist-page-container background">
            {isLoaded ? (
                <div className="artist-page page-load-transition background">
                    <div className="artist-info-section l-horizontal">
                        <div className="artist-image-section l-horizontal">
                            <img className="artist-image rounded shadowed" src={currentArtist.image} height="200px" alt="artist portrait"></img>
                        </div>
                        <div className="artist-details">
                            <p className="artist-heading">Artist</p>
                            <p className="artist-name">{currentArtist.title}</p>
                            <p className="artist-followers">{`${currentArtist.numFollowers} Following`}</p>
                        </div>
                    </div>
                    <div className="artist-bio-section background">
                        <p className="artist-bio-header">Biography</p>
                        <p className="artist-bio">{currentArtist.bio}</p>
                    </div>
                    <div className="artist-most-played">
                        <div className="artist-tracks-heading">
                            <p className="artist-tracks-heading-text">Popular Tracks</p>
                        </div>
                        <TrackContainer tracks={artistTracks} category='user' />
                    </div>
                    <div className="artist-albums">
                        <GeneralListingContainer title={`${currentArtist.title}'s Albums`} listings={artistAlbums} category="Album" />
                    </div>
                </div>
            ) : (
                <LoadingPage />
            )}
        </div>
    )
}
