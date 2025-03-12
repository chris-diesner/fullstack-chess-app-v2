import {User} from "../models/User";

interface ChessAppState {
    userDetails: User | null;
}

const initialState: ChessAppState = {
    userDetails: null
}

interface Action {
    type: string;
    payload?: User;
}

const chessAppReducer = (state = initialState, action: Action) => {
    switch (action.type) {
        case 'SET_USER_DETAILS':
            return {
                ...state,
                userDetails: action.payload
            }
        default:
            return state
    }
}

export default chessAppReducer;