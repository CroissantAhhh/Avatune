// import { csrfFetch } from "./csrf";
const LOAD = 'artists/LOAD';
const ADD = 'artists/ADD';
const REMOVE = 'artists/REMOVE';

const load = list => ({
    type: LOAD,
    list,
});

const add = (artist) => ({
    type: ADD,
    artist,
});

export const loadUserArtists = (userId) => async dispatch => {
    const response = await fetch(`/api/artists/byUser/${userId}`);

    if (response.ok) {
        const artists = await response.json();
        dispatch(load(artists.artists));
    };
};

export const loadArtistByHash = (artistHash) => async dispatch => {
    const response = await fetch(`/api/artists/byHash/${artistHash}`);

    if (response.ok) {
        const artists = await response.json();
        dispatch(load(artists.artists));
        return artists.artists[0].id;
    };
}

const artistReducer = (state = {}, action) => {
    switch (action.type) {
        case LOAD:
            const newState = {};
            for (let item of action.list) {
                newState[item.id] = item;
            };
            return newState;
        case ADD:
            return {...state, [action.artist.id]: action.artist}
        default:
            return state;
    }
};

export default artistReducer;
