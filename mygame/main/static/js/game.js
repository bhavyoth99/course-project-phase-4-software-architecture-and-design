var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

var game = new Phaser.Game(config);

function preload() {
    this.load.image('red_card', 'static/img/logo.png');
    this.load.image('black_card', 'static/img/logo2.png');
}


function create() {
    this.cards = [
        this.add.sprite(100, 300, 'red_card').setInteractive(),
        this.add.sprite(250, 300, 'red_card').setInteractive(),
        this.add.sprite(400, 300, 'black_card').setInteractive(),
        this.add.sprite(550, 300, 'black_card').setInteractive()
    ];

    this.cards.forEach(card => card.on('pointerdown', changeCard, this));

    // Define a property to control the scale direction
    this.scaleDirection = 1;

    this.instructionText = this.add.text(100, 100, 'Choose 4 red cards!', { fontSize: '32px', fill: '#000' });

    this.submitButton = this.add.text(500, 500, 'Submit', { fontSize: '32px', fill: '#000' }).setInteractive();
    this.submitButton.on('pointerdown', checkCards, this);
}


function update() {
    // If the text is too big, switch direction
    if (this.instructionText.scaleX > 1.2) {
        this.scaleDirection = -1;
    }
    // If the text is too small, switch direction
    else if (this.instructionText.scaleX < 1) {
        this.scaleDirection = 1;
    }

    // Scale the text up or down based on the current direction
    this.instructionText.scaleX += 0.005 * this.scaleDirection;
    this.instructionText.scaleY += 0.005 * this.scaleDirection;
}


function changeCard(card) {
    if (card.texture.key === 'red_card') {
        card.setTexture('black_card');
    } else {
        card.setTexture('red_card');
    }
}


function checkCards() {
    var allRed = this.cards.every(card => card.texture.key === 'red_card');
    if (allRed) {
        this.instructionText.setText('You win! All cards are red.');
    } else {
        this.instructionText.setText('Try again! All cards must be red.');
    }
}
