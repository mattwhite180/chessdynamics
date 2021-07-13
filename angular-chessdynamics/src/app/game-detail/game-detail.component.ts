import { Component, OnInit, Input } from '@angular/core';
import { Game } from '../game';
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
  legal_moves: any;
  board: any;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getGame();
    this.board = ChessBoard('board1', {
      position: "empty", //this.game!.fen,
      draggable: true
    });
  }

  refreshBoard(): void {
    this.getGame();
    this.board = ChessBoard('board1', {
      position: this.game!.fen, //this.game!.fen,
      draggable: true
    });
    this.legal_moves = this.game!.legal_moves.split(",");
  }
  
  getGame(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.getGame(id)
      .subscribe(game => this.game = game);
  }

  save(): void {
    if (this.game) {
      this.gameService.updateGame(this.game)
        .subscribe(() => this.goBack());
    }
  }

  playTurn(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.apiAction(id, "play_turn").subscribe();
  }

  playMove(move: String): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.apiAction(id, "play_move/" + move).subscribe();
  }

  goBack(): void {
    this.location.back();
  }

}
