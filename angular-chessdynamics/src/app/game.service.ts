import { Injectable } from '@angular/core';
import { Game } from './game';
import { GAMES } from './mock-games';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';


@Injectable({
  providedIn: 'root'
})

export class GameService {

  constructor(private messageService: MessageService) { }

  getGames(): Observable<Game[]> {
    const games = of(GAMES);
    this.messageService.add('GameService: fetched games');
    return games;
  }
  
  getGame(id: number): Observable<Game> {
    // For now, assume that a game with the specified `id` always exists.
    // Error handling will be added in the next step of the tutorial.
    const game = GAMES.find(g => g.id === id)!;
    this.messageService.add(`GameService: fetched game id=${id}`);
    return of(game);
  }
}
