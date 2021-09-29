import { Component, OnInit, Input } from '@angular/core';
import { Game } from '../game';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { GameService } from '../game.service';

@Component({
  selector: 'app-game-detail',
  templateUrl: './game-detail.component.html',
  styleUrls: ['./game-detail.component.css'],
})
export class GameDetailComponent implements OnInit {
  game: Game | undefined;
  legal_moves: any;

  constructor(
    private route: ActivatedRoute,
    private gameService: GameService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getGame();
    this.myLoop();
  }

  async myLoop(): Promise<void> {
    while (true) {
      await sleep(1000);
      console.log("im in refresh!")
      if ((this.game?.refresh == true) && (this.game?.results == "*")) {
        console.log("refreshing!")
        this.getGame()
      }
    }
  }

  refreshBoard(): void {
    this.getGame();
  }

  async refresh(): Promise<void> {
    await sleep(600);
    this.getGame();
  }

  getGame(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.getGame(id).subscribe((game) => (this.game = game));
  }

  save(): void {
    if (this.game) {
      this.gameService.updateGame(this.game).subscribe(() => this.goBack());
    }
    this.getGame();
  }

  playLeela(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.apiAction(id, 'play_leela').subscribe();
    this.refresh();
  }

  playStockfish(level: String): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.apiAction(id, 'play_stockfish/' + level).subscribe();
    this.refresh();
  }

  delete(game: Game): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.deleteGame(id).subscribe();
  }

  pop(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.apiAction(id, 'pop').subscribe();
    this.refresh();
  }

  playMove(move: String): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.gameService.apiAction(id, 'play_move/' + move).subscribe();
    this.refresh();
  }

  goBack(): void {
    this.location.back();
  }
}

function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}
