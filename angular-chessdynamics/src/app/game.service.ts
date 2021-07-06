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

  private gamesUrl = 'http://localhost:8000/games/'

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

  apiAction(id: number, func: String): any {
    const url = `${this.gamesUrl}${id}/${func}/`;
    return this.http.get(url).pipe(
      tap(_ => this.log(`playing game...`)),
      catchError(this.handleError(`playing game...`))
    );
  }
}
