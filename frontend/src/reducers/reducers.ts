import {combineReducers} from 'redux';
import chessAppReducer from "./ChessAppReducer";

const rootReducer = combineReducers({
    chessApp: chessAppReducer
})
export default rootReducer;