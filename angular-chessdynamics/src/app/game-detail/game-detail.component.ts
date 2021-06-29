import { Component, OnInit, Input } from '@angular/core';
import { Game } from '../game'

@Component({
  selector: 'app-game-detail',
  templateUrl: './game-detail.component.html',
  styleUrls: ['./game-detail.component.css']
})
export class GameDetailComponent implements OnInit {

  constructor() { }

  @Input() game?: Game;

  ngOnInit(): void {
  }

}
