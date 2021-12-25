// import { csrfFetch } from "./csrf";
const LOAD = 'albums/LOAD';
const ADD = 'albums/ADD';
const REMOVE = 'albums/REMOVE';

const load = list => ({
    type: LOAD,
    list,
});

const add = (album) => ({
    type: ADD,
    album,
});

export const loadUserAlbums = (userId) => async dispatch => {
    const response = await fetch(`/api/albums/byUser/${userId}`);

    if (response.ok) {
        const albums = await response.json();
        dispatch(load(albums.albums));
    };
};

export const loadAlbumByHash = (albumHash) => async dispatch => {
    const response = await fetch(`/api/albums/byHash/${albumHash}`);

    if (response.ok) {
        const albums = await response.json();
        dispatch(load(albums.albums));
        return albums.albums[0];
    }
}

export const loadMediaAlbums = (mediumID) => async dispatch => {
    const response = await fetch(`/api/albums/byMedia/${mediumID}`);

    if (response.ok) {
        const albums = await response.json();
        dispatch(load(albums.albums))
    }
}

export const loadArtistAlbums = (artistID) => async dispatch => {
    const response = await fetch(`/api/albums/byArtist/${artistID}`);

    if (response.ok) {
        const albums = await response.json();
        dispatch(load(albums.albums))
    }
}

export const loadSearchAlbums = (searchQuery) => async dispatch => {
    const response = await fetch(`/api/albums/search/${searchQuery}`);

    if (response.ok) {
        const albums = await response.json();
        dispatch(load(albums.albums))
    }
}

export const loadSearchAlbumsFull = (searchQuery) => async dispatch => {
    const response = await fetch(`/api/albums/fullSearch/${searchQuery}`);

    if (response.ok) {
        const albums = await response.json()
        dispatch(load(albums.albums))
    }
}

export const getLatestAlbum = () => async dispatch => {
    const response = await fetch(`/api/albums/latest`);

    if (response.ok) {
        const album = await response.json()
        dispatch(add(album.albums))
    }
}

const albumReducer = (state = {}, action) => {
    switch (action.type) {
        case LOAD:
            const newState = {};
            for (let item of action.list) {
                newState[item.id] = item;
            };
            return newState;
        case ADD:
            return {...state, [action.album.id]: action.album}
        default:
            return state;
    }
};

export default albumReducer;
