// import { csrfFetch } from "./csrf";
const LOAD = 'media/LOAD';
const ADD = 'media/ADD';
const REMOVE = 'media/REMOVE';

const load = list => ({
    type: LOAD,
    list,
});

const add = (media) => ({
    type: ADD,
    media
});

export const loadUserMedia = (userId) => async dispatch => {
    const response = await fetch(`/api/media/byUser/${userId}`);

    if (response.ok) {
        const media = await response.json();
        dispatch(load(media.media));
    };
};

export const loadUserMediaMost = (userId) => async dispatch => {
    const response = await fetch(`/api/media/byUserMost/${userId}`);

    if (response.ok) {
        const media = await response.json();
        dispatch(load(media.media))
    }
}

const mediaReducer = (state = {}, action) => {
    switch (action.type) {
        case LOAD:
            const newState = {};
            for (let item of action.list) {
                newState[item.id] = item;
            };
            return newState;
        case ADD:
            return {...state, [action.media.id]: action.media }
        default:
            return state;
    }
};

export default mediaReducer;
