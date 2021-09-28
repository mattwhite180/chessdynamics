export interface Game {
    id: number;
    name: string;
    description: string;
    move_list: string;
    white: string;
    black: string;
    time_controls: number;
    results: string;
    available: boolean;
    turn: string;
    fen: string;
    legal_moves: string;
    legal_moves_list: string[];
    creation_date: string;
    board: any;
    last_move: string;
    refresh: boolean;
  }