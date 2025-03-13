import { User } from './User';

export type Lobby = {
    game_id: string;
    players: User[];
    };