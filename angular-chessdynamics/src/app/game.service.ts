import { Injectable } from '@angular/core';
import { Game } from './game';
import { GAMES } from './mock-games';
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})

export class GameService {

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  private gamesUrl = 'http://localhost:4000/games/'

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }


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
    return this.http.get<Game[]>(this.gamesUrl)
      .pipe(
        tap(_ => this.log('fetched games')),
        catchError(this.handleError<Game[]>('getGames', []))
      );
  }
  
  private log(message: string) {
    this.messageService.add(message);
  }

  getGame(id: number): Observable<Game> {
    const url = `${this.gamesUrl}${id}/`;
    return this.http.get<Game>(url).pipe(
      tap(_ => this.log(`fetched game id=${id}`)),
      catchError(this.handleError<Game>(`getGame id=${id}`))
    );
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
      tap(_ => this.log(`updated game id=${game.id}`)),
      catchError(this.handleError<any>('updateGame'))
    );
  }

  apiAction(id: number, func: String): any {
    const url = `${this.gamesUrl}${id}/${func}/`;
    this.log("calling " + String(url));
    return this.http.get(url).pipe(
      tap(_ => this.log(`got response from ` + String(url))),
      catchError(this.handleError(`error from ` + String(url)))
    );
  }
}
