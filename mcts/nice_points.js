/**
 * Created by Renan on 14-Oct-15.
 */

var RESULT = {WIN : 1, DRAW : 0.5, LOST : 0};
var C = 0.3;
var EPSILON = 0.1;

function GameState(n, counter, edges, playerJustMoved, currentPlayer){ // NOTE how to generalize this to the rootnode be anywhere?
    var self = this;

    self.n = n;
    // pretend the opponent just moved, player 0 makes the move now
    self.playerJustMoved = (typeof playerJustMoved !== 'undefined') ? playerJustMoved : 1;
    self.currentPlayer = (typeof currentPlayer !== 'undefined') ? currentPlayer : 0;
    self.counter = counter;
    self.edges = edges;

    self.clone = function(){
        return new GameState(self.n, self.counter.slice(0), self.edges.slice(0), self.playerJustMoved, self.currentPlayer);
    };
    self.madeSquare = function(move){
        var numSquaresMade = 0;
        var N = self.n;
        // horizontal edge
        if(move < N*(N-1)){
            var a = Math.floor(move/(N-1));
            var b = move%(N-1);
            var p = n*(n-1) + (a-1)*n + b; // the left edge of the above square
            // square above
            if(move - N + 1 > 0){
                if( self.edges[p] == 1 && self.edges[move - N + 1] == 1 && self.edges[p+1] == 1) numSquaresMade++;
            }
            // square below
            if(move + N - 1 < N*(N - 1)){
                if(self.edges[p + N] == 1 && self.edges[move + N -1] == 1 && self.edges[p + N + 1] == 1) numSquaresMade++;
            }
        }
        // vertical
        else{
            var m = move - N*(N - 1);
            var a = Math.floor(m / N);
            var b = m % N;
            var p = b - 1 + a*(N - 1); // the top edge of the left square
            // left square
            if(move - N*(N - 1) % N !== 0){
                if(self.edges[p + N - 1] == 1 && self.edges[move - 1] == 1 && self.edges[p] == 1) numSquaresMade++;
            }
            // right square
            if(move - N*(N - 1) % N !== N - 1){
                if(self.edges[p + 1] == 1 && self.edges[move + 1] == 1 && self.edges[p + N] == 1) numSquaresMade++;
            }
        }
        return numSquaresMade;
    };
    self.doMove = function(move) {
        self.edges[move] = 1;
        self.playerJustMoved = self.currentPlayer;
        var squares = self.madeSquare(move);
        if(squares === 0) self.currentPlayer = 1 - self.currentPlayer;
        else self.counter[self.playerJustMoved] += squares;
    };
    self.doRandomMove = function(){
        var moves = self.getMoves();
        var m = moves[Math.floor(Math.random()*moves.length)];
        self.doMove(m);
    };
    self.getMoves = function(){
        var result = [];
        for(var i = 0; i < self.edges.length; i++){
            if(self.edges[i] === 0) result[result.length] = i;
        }
        return result;
    };
    self.gameEnded = function(){
        for(var i = 0; i < self.edges.length; i++){
            if(self.edges[i] === 0) return false;
        }
        return true;
    }
    self.getResult = function(pjm){ // TODO this part is critical; this function can't be called in a non-terminal state.
        if(self.counter[pjm] > self.counter[1 - pjm]) return RESULT.WIN;
        else if(self.counter[pjm] === self.counter[1 - pjm]) return RESULT.DRAW;
        else return RESULT.LOST;
    };
}

function Node(state, move, parent){
    var self = this;

    self.move = typeof move !== 'undefined' ? move : null;
    self.parent = typeof parent !== 'undefined' ? parent : null;
    self.state = typeof state !== 'undefined' ? state : null;

    self.childNodes = [];
    self.wins = 0;
    self.draws = 0; // NOTE included since this is not a zero-sum game
    self.visits = 0;
    self.untriedMoves = self.state.getMoves();
    self.playerJustMoved = self.state.playerJustMoved;
    self.currentPlayer = self.state.currentPlayer;

    this.ucb = function(){
        if(self.visits !== 0) return (self.wins + 0.5*self.draws)/self.visits + C*Math.sqrt(Math.log(self.parent.visits/self.visits));
        else throw "ucb should not be called for a node with untried moves."
    };

    self.uctSelectChild = function() {
        var bestChild = null;
        var bestValue = -Infinity;
        for(var i = 0; i < self.childNodes.length; i++){
            if(self.childNodes[i].ucb() > bestValue){
                bestChild = self.childNodes[i];
                bestValue = self.childNodes[i].ucb();
            }
        }
        return bestChild;
    };

    self.addChild = function(move, state){
        var node = new Node(state, move, this);
        self.untriedMoves.splice(self.untriedMoves.indexOf(move), 1); // TODO test this
        self.childNodes[self.childNodes.length] = node; // all these nodes are the same?
        return node;
    };

    self.update = function(result){
        self.visits++;
        if(result === RESULT.WIN) self.wins += 1;
        else if(result === RESULT.DRAW) self.draws += 1;
    };

    self.getBestChild = function(){
        var bestChild = null;
        var biggestNumVisits = -Infinity;
        for(var i = 0; i < self.childNodes.length; i++){
            if(self.childNodes[i].visits > biggestNumVisits){
                bestChild = self.childNodes[i];
                biggestNumVisits = self.childNodes[i].visits;
            }
        }
        return bestChild;
    };
}

var uct = function(rootstate, itermax, move){
    var rootnode = new Node(rootstate, typeof move !== 'undefined' ? move : null, null);

    for(var i = 0; i < itermax; i++){
        var node = rootnode;
        var state = rootstate.clone();
        // Selection
        // if the node is a non-terminal and fully-expanded
        while(node.untriedMoves.length === 0 && node.childNodes.length > 0){
            node = node.uctSelectChild();
            state.doMove(node.move)
        }
        // Expansion
        // if we can still expand it
        if(node.untriedMoves != []){
            var moves = node.untriedMoves;
            var m = moves[Math.floor(Math.random()*moves.length)];
            state.doMove(m);
            // add child and descent tree
            node = node.addChild(m, state);
        }
        // Exploration
        // TODO doRandomRollout())
        var moves = state.getMoves();
        while (moves.length !== 0){
            state.doRandomMove();
            moves = state.getMoves();
        }
        // Backpropagation
        // backpropagate from the expanded node and work back to the root node
        if(!state.gameEnded()) throw "the game didn't end"
        while (node !== null){
            // state is terminal. Update node with result from POV of node.playerJustMoved
            node.update(state.getResult(node.playerJustMoved));
            node = node.parent;
        }
    }

    return rootnode.getBestChild();
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// TESTS

//var otherEdges = function(n, i) {;
//    var a = Math.floor(i/(n-1));
//    var b = i%(n-1);
//    //console.log(a, b);
//    var e = n*(n-1) + (a-1)*n + b;
//    var d = e + 1;
//    var o = i + n-1;
//    console.log(e, o, d);
//}
//otherEdges(5, 9);
//otherEdges(5, 3);
//otherEdges(5, 11);

// test GameState constructor and clone function
//var n = 3;
//var counter = [0,0];
//var edges = [];
//for (var i = 0; i < 2*n*(n - 1); i++) edges[i] = 0;
//var gs1 = new GameState(n, counter, edges);
//var gs2 = gs1.clone();
//
//// test completing one square
//var gs3 = new GameState(n, [0,0], [1,0,1,0,0,0,1,0,0,0,0,0]);
//var node1 = new Node(gs3, 2, null);
//var gs4 = gs3.clone();
//gs4.doMove(7);
//var node2 = node1.addChild(7, gs4);
//console.log(node2.state.counter);
//
//// test completing 2 squares at once
//var gs5 = new GameState(3, [0,0], [1,1,1,1,0,0,1,0,1,0,0,0]);
//var node3 = new Node(gs5, 2, null);
//gs5.doMove(7);
//var node4 = node3.addChild(7, gs5);
//console.log(node4.state.counter);

// to show that Math.random has an uniform distribuition
//var numbers = [0,0,0,0,0];
//var num;
//for(var i = 0; i < 1000000; i++){
//    num = Math.floor(Math.random()*numbers.length);
//    numbers[num] += 1;
//}
//var sum = 0;
//for(var i = 0; i<numbers.length; i++){
//    sum += numbers[i];
//}
//var normSum = sum/numbers.length;
//for(var i = 0; i<numbers.length; i++){
//    numbers[i] /= normSum;
//}


var n = 3;
//var edges = [];
//for (var i = 0; i < 2*n*(n - 1); i++) edges[i] = 0;
var edges = [1,1,0,0,1,0,1,0,1,1,0,1];
var gs6 = new GameState(n, [0,0], edges);
var node5 = uct(gs6, 5000, 2);

console.log(node5.move);