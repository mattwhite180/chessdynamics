#!/bin/bash

git clone https://github.com/jhlywa/chess.js

npm install
# npm install --save-dev @angular-devkit/build-angular
# npm install --save @angular-devkit/build-angular
npm install -g @angular/cli@latest --save
npm install chessboardjs --save
npm install jquery --save

ng build

ng serve --host 0.0.0.0