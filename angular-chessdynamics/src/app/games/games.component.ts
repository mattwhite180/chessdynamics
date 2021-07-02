import { Component, OnInit } from '@angular/core';
import { Game } from '../game';
import { GAMES } from '../mock-games';
import { GameService } from '../game.service';
import { MessageService } from '../message.service';


@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.css']
})
export class GamesComponent implements OnInit {

  selectedGame?: Game;

  games: Game[] = [];

  constructor(
    private gameService: GameService,
    private messageService: MessageService) { }

  ngOnInit(): void {
    this.getGames();
  }

  onSelect(game: Game): void {
    this.selectedGame = game;
    this.messageService.add(`GamesComponent: Selected game id=${game.id}`);
  }

  getGames(): void {
    this.gameService.getGames()
        .subscribe(games => this.games = games);
  }

}
