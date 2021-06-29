import { Component, OnInit } from '@angular/core';
import { Game } from '../game';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.css']
})
export class GamesComponent implements OnInit {

  constructor() { }

  game: Game = {
    id: 1,
    name: 'Agadmator'
  };

  ngOnInit(): void {
  }

}
