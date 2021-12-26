import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams, useHistory } from 'react-router-dom';

import { loadAlbumByHash } from '../../store/albums';
import { loadAlbumTracks } from '../../store/tracks';

import { useBrowsingHistory } from '../../context/BrowsingHistoryContext';

import LoadingPage from '../LoadingPage';
import TrackContainer from '../../components/TrackContainer';
import GeneralListingContainer from '../../components/GeneralListingContainer';

import './AlbumPage.css';

export default function AlbumPage() {
    const [isLoaded, setIsLoaded] = useState(false);
    const dispatch = useDispatch();
    const history = useHistory();
    const { albumHash } = useParams();
    const { nextLocation } = useBrowsingHistory();
    const [mediumAlbums, setMediumAlbums] = useState();
    const [artistAlbums, setArtistAlbums] = useState();

    function nextPath(path) {
        nextLocation(path);
        history.push(path);
    }

    useEffect(() => {
        (async() => {
            setIsLoaded(false);
            const currentAlbum = await dispatch(loadAlbumByHash(albumHash))
            await dispatch(loadAlbumTracks(currentAlbum.id));
            const fetch1 = await fetch(`/api/albums/byMedia/${currentAlbum.medium.id}`);
            const response1 = await fetch1.json();
            setMediumAlbums(response1.albums.filter(album => album.id !== currentAlbum.id));
            const fetch2 = await fetch(`/api/albums/byArtist/${currentAlbum.artists[0].id}`);
            const response2 = await fetch2.json();
            setArtistAlbums(response2.albums.filter(album => album.id !== currentAlbum.id));
            setIsLoaded(true);
        })()
    }, [dispatch, albumHash])
    // Album information section

    // Album tracks

    // More by the main artist (the first one)
    const album = useSelector(state => Object.values(state.albums))[0];
    const albumTracks = useSelector(state => Object.values(state.tracks));

    function totalDuration() {
        const totalSeconds = albumTracks.reduce((prev, curr) => prev + curr.duration, 0);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes =  Math.floor((totalSeconds - hours * 3600) / 60);
        const seconds = totalSeconds % 60;
        const hoursStr = hours > 0 ? `${hours} hours ` : '';
        const minutesStr = `${minutes} minutes `;
        const secondsStr = seconds > 0 ? `${seconds} seconds` : '';
        return hoursStr + minutesStr + secondsStr;
    };

    return (
        <div className="album-page-container background">
            {isLoaded ? (
                <div className="album-page page-load-transition">
                    <div className="album-header l-horizontal">
                        <div className="album-image-section l-horizontal">
                            <img className="album-image shadowed" src={album.image} height="250px" alt="album artwork" />
                        </div>
                        <div className="album-detailed-info">
                            <p className="album-heading">Album</p>
                            <p className="album-title">{album.title}</p>
                            <div className="album-info-numbers">
                                {album.artists.map(artist => (
                                    <p className="album-artist-link hover-pointer link-hover" onClick={() => nextPath(`/artist/${artist.hashedId}`)}>{artist.title}</p>
                                ))}
                                <p className="album-songs-info">{`· ${albumTracks.length} songs, ${totalDuration()}`}</p>
                            </div>
                        </div>
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
