import {User} from '../models/User';

export const setUserDetails = (user: User) => {
    return {
        type: 'SET_USER_DETAILS',
        payload: user
    }
}