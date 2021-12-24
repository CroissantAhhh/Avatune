// import { csrfFetch } from "./csrf";
const LOAD = 'users/LOAD';
const ADD = 'users/ADD';
const REMOVE = 'users/REMOVE';

const load = list => ({
    type: LOAD,
    list,
});

const add = (list) => ({
    type: ADD,
    list,
});

export const loadUser = (userId) => async dispatch => {
    const response = await fetch(`/api/users/${userId}`);

    if (response.ok) {
        const users = await response.json();
        dispatch(load(users.users));
    };
};

export const loadUserByHash = (userHash) => async dispatch => {
    const response = await fetch(`/api/users/byHash/${userHash}`);

    if (response.ok) {
        const users = await response.json();
        users.users[0].categories = [ "main" ];
        dispatch(load(users.users));
        return users.users[0].id;
    };
}

export const loadUserFollowers = (userId) => async dispatch => {
    const response = await fetch(`/api/users/followers/${userId}`);

    if (response.ok) {
        const users = await response.json();
        dispatch(load(users.users))
    }
}

export const addUserFollows = (userId) => async dispatch => {
    const followers = await fetch(`/api/users/followers/${userId}`);
    const following = await fetch(`/api/users/following/${userId}`);

    if (followers.ok && following.ok) {
        const userFollowers = await followers.json();
        const userFollowing = await following.json();
        console.log(userFollowers.users)
        console.log(userFollowing.users)
        const userFollows = [];
        for (let follower of userFollowers.users) {
            follower.categories = ['follower'];
            userFollows.push(follower);
        }
        for (let followed of userFollowing.users) {
            if (userFollows.find(user => user.id === followed.id)) {
                const userIndex = userFollows.findIndex(user => user.id === followed.id);
                userFollows[userIndex].categories.push('following');
            } else {
                followed.categories = ['following'];
                userFollows.push(followed);
            }
        }
        dispatch(add(userFollows))
    }
}

export const loadUserFollowing = (userId) => async dispatch => {
    const response = await fetch(`/api/users/following/${userId}`);

    if (response.ok) {
        const users = await response.json();
        dispatch(load(users.users))
    }
}

const usersReducer = (state = {}, action) => {
    switch (action.type) {
        case LOAD:
            const newState = {};
            for (let item of action.list) {
                newState[item.id] = item;
            };
            return newState;
        case ADD:
            const newStateAdd = {...state};
            for (let item of action.list) {
                newStateAdd[item.id] = item;
            };
            return newStateAdd;
        default:
            return state;
    }
};

export default usersReducer;
