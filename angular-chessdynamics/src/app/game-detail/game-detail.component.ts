import { Component, OnInit, Input } from '@angular/core';
import { Game } from '../game'
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { GameService } from '../game.service';

declare var ChessBoard: any;

@Component({
  selector: 'app-game-detail',
  templateUrl: './game-detail.component.html',
  styleUrls: ['./game-detail.component.css']
})
export class GameDetailComponent implements OnInit {

  game: Game | undefined;
  board: any;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getGame();
    let myFen = "start";
    if (typeof this.game?.fen != "undefined") {
      myFen = this.game.fen;
    }
    this.board = ChessBoard('board1', {
      position: myFen,
      draggable: true
    });
  }
  
  getGame(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.getGame(id)
      .subscribe(game => this.game = game);
  }

  goBack(): void {
    this.location.back();
  }

}
