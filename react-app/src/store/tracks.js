// import { csrfFetch } from "./csrf";
const LOAD = 'tracks/LOAD';
const ADD = 'tracks/ADD';
const REMOVE = 'tracks/REMOVE';

const load = list => ({
    type: LOAD,
    list,
});

const add = (track) => ({
    type: ADD,
    track,
});

export const loadUserTracks = (userId) => async dispatch => {
    const response = await fetch(`/api/tracks/byUser/${userId}`);

    if (response.ok) {
        const tracks = await response.json();
        dispatch(load(tracks.tracks));
    };
};

export const loadAlbumTracks = (albumId) => async dispatch => {
    const response = await fetch(`/api/tracks/byAlbum/${albumId}`);

    if (response.ok) {
        const tracks = await response.json();
        dispatch(load(tracks.tracks));
    }
}
export const loadUserTracksMost = (userId) => async dispatch => {
    const response = await fetch(`/api/tracks/userMost/${userId}`);

    if (response.ok) {
        const tracks = await response.json();
        dispatch(load(tracks.tracks));
    };
};

export const loadUserTracksRecent = (userId) => async dispatch => {
    const response = await fetch(`/api/tracks/userRecent/${userId}`);

    if (response.ok) {
        const tracks = await response.json();
        dispatch(load(tracks.tracks));
    };
};

export const loadPlaylistTracks = (playlistId) => async dispatch => {
    const response = await fetch(`/api/tracks/byPlaylist/${playlistId}`);

    if (response.ok) {
        const tracks = await response.json();
        dispatch(load(tracks.tracks));
    };
};

const trackReducer = (state = {}, action) => {
    switch (action.type) {
        case LOAD:
            const newState = {};
            for (let item of action.list) {
                newState[item.id] = item;
            };
            return newState;
        case ADD:
            return {...state, [action.track.id]: action.track}
        default:
            return state;
    }
};

export default trackReducer;
