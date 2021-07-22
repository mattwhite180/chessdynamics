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
}
