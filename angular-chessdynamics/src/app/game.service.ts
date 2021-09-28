import { Injectable } from '@angular/core';
import { Game } from './game';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

declare var ChessBoard: any;
declare var Chess: any;

@Injectable({
  providedIn: 'root',
})
export class GameService {
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  };

  private gamesUrl = 'http://localhost:8000/games/';
  // private gamesUrl = 'http://localhost:5000/games/';

  constructor(
    private http: HttpClient,
    private messageService: MessageService
  ) {}

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  getGames(): Observable<Game[]> {
    return this.http.get<Game[]>(this.gamesUrl).pipe(
      tap((_) => this.log('fetched games')),
      catchError(this.handleError<Game[]>('getGames', []))
    );
  }

  private log(message: string) {
    this.messageService.add(message);
  }

  getGame(id: number): Observable<Game> {
    const url = `${this.gamesUrl}${id}/`;
    return this.http.get<Game>(url).pipe(
      tap((_) => this.log(`fetched game id=${id}`)),
      catchError(this.handleError<Game>(`getGame id=${id}`)),
      map((g) => this.modify(g, this.http, this.gamesUrl))
    );
  }

  modify(gamemodel: Game, http: any, url: string) {
    ////////////////////////////////////////////////////////////////////////
    function onDragStart(
      source: any,
      piece: any,
      position: any,
      orientation: any
    ) {
      // do not pick up pieces if the game is over
      if (gamemodel["results"] !== "*") return false;

      // only pick up pieces for the side to move
      if (
        (gamemodel["turn"] === 'white' && piece.search(/^b/) !== -1) ||
        (gamemodel["turn"] === 'black' && piece.search(/^w/) !== -1)
      ) {
        return false;
      }
      return true;
    }

    var onDrop = function(source: any, target: any) : any {
      // see if the move is legal
      var move = source + target;
      var moveList = gamemodel['legal_moves'].split(',');
      for (var i = 0; i < moveList.length; i++) {
        if (moveList[i] === move) {
          const func = "play_move/" + move;
          const myurl = `${url}${gamemodel['id']}/${func}/`;
          gamemodel['refresh'] = true;
          return http.get(myurl).pipe().subscribe();
        }
      }
      return 'snapback';
    }

    // update the board position after the piece snap
    // for castling, en passant, pawn promotion
    function onSnapEnd() {
      // game.position(game.fen());
      return 'snapback';
    }

    var config = {
      draggable: gamemodel['available'],
      orientation: gamemodel['turn'],
      position: gamemodel['fen'],
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd
    };

    ////////////////////////////////////////////////////////////////////////
    gamemodel['board'] = ChessBoard('board1', config);
    var legal_moves = gamemodel['legal_moves'].split(',');
    gamemodel['legal_moves_list'] = legal_moves;
    gamemodel['last_move'] = legal_moves[legal_moves.length - 1];
    gamemodel['refresh'] = (!gamemodel['available']);
    // this.legal_moves = this.game!.legal_moves.split(",");
    return gamemodel;
  }

  addGame(game: Game): Observable<Game> {
    return this.http.post<Game>(this.gamesUrl, game, this.httpOptions).pipe(
      tap((newGame: Game) => this.log(`added game w/ id=${newGame.id}`)),
      catchError(this.handleError<Game>('addGame'))
    );
  }

  updateGame(game: Game): Observable<any> {
    const url = `${this.gamesUrl}${game.id}/`;
    return this.http.put(url, game, this.httpOptions).pipe(
      tap((_) => this.log(`updated game id=${game.id}`)),
      catchError(this.handleError<any>('updateGame'))
    );
  }

  deleteGame(id: number): Observable<Game> {
    const url = `${this.gamesUrl}${id}/`;

    return this.http.delete<Game>(url, this.httpOptions).pipe(
      tap((_) => this.log(`deleted game id=${id}`)),
      catchError(this.handleError<Game>('deleteGame'))
    );
  }

  apiAction(id: number, func: String): any {
    const url = `${this.gamesUrl}${id}/${func}/`;
    this.log('calling ' + String(url));
    return this.http.get(url).pipe(
      tap((_) => this.log(`got response from ` + String(url))),
      catchError(this.handleError(`error from ` + String(url)))
    );
  }
}
