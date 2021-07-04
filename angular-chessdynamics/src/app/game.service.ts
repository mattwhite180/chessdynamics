import { Injectable } from '@angular/core';
import { Game } from './game';
import { GAMES } from './mock-games';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class GameService {

  private gamesUrl = 'http://localhost:8000/games/'

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  // getGames(): Observable<Game[]> {
  //   const games = of(GAMES);
  //   this.log('GameService: fetched games');
  //   return games;
  // }

  getGames(): Observable<Game[]> {
    return this.http.get<Game[]>(this.gamesUrl)
  }
  
  private log(message: string) {
    this.messageService.add(message);
  }

  getGame(id: number): Observable<Game> {
    // For now, assume that a game with the specified `id` always exists.
    // Error handling will be added in the next step of the tutorial.
    const game = GAMES.find(g => g.id === id)!;
    this.log(`GameService: fetched game id=${id}`)
    return of(game);
  }
}
