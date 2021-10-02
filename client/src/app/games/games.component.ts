import { Component, OnInit } from '@angular/core';
import { Game } from '../game';
import { GameService } from '../game.service';
import { MessageService } from '../message.service';


@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.css']
})
export class GamesComponent implements OnInit {

  games: Game[] = [];

  constructor(
    private gameService: GameService) { }

  ngOnInit(): void {
    this.getGames();
  }

  delete(game: Game): void {
    this.games = this.games.filter(h => h !== game);
    this.gameService.deleteGame(game.id).subscribe();
  }

  getGames(): void {
    this.gameService.getGames()
        .subscribe(games => this.games = games);
  }

  add(name: string, description: string, white: string, black: string, tc: string): void {
    name = name.trim();
    const time_controls = +tc;
    if (!name) { return; }
    this.gameService.addGame({name, description, white, black, time_controls} as Game)
      .subscribe(game => {
        this.games.push(game);
      });
  }

}
