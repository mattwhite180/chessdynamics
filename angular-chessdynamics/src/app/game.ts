export interface Game {
    id: number;
    name: string;
    description: string;
    move_list: string;
    white: string;
    white_level: number;
    black: string;
    black_level: number;
    time_controls: number;
    results: string;
    fen: string;
    legal_moves: string;
    legal_moves_list: string[];
    creation_date: string;
    board: any;
    available: boolean;
    turn: string;
  }