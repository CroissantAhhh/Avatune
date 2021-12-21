// import { csrfFetch } from "./csrf";
const LOAD = 'playlists/LOAD';
const ADD = 'playlists/ADD';
const REMOVE = 'playlists/REMOVE';

const load = list => ({
    type: LOAD,
    list,
});

const add = (playlist) => ({
    type: ADD,
    playlist,
});

export const loadUserPlaylists = (userId) => async dispatch => {
    const response = await fetch(`/api/playlists/byUser/${userId}`);

    if (response.ok) {
        const playlists = await response.json();
        dispatch(load(playlists.playlists));
    };
};

export const loadUserPlaylistsMost = (userId) => async dispatch => {
    const response = await fetch(`/api/playlists/byUserMost/${userId}`);

    if (response.ok) {
        const playlists = await response.json();
        dispatch(load(playlists.playlists));
    };
};

export const loadPlaylistByHash = (playlistHash) => async dispatch => {
    const response = await fetch(`/api/playlists/byHash/${playlistHash}`);

    if (response.ok) {
        const playlists = await response.json();
        dispatch(load(playlists.playlists));
        return playlists.playlists[0].id;
    }
}

const playlistReducer = (state = {}, action) => {
    switch (action.type) {
        case LOAD:
            const newState = {};
            for (let item of action.list) {
                newState[item.id] = item;
            };
            return newState;
        case ADD:
            return {...state, [action.playlist.id]: action.playlist}
        default:
            return state;
    }
};

export default playlistReducer;
