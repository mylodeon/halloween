var gpio = require('rpi-gpio');
var express = require('express')
var cors = require('cors')
var app = express()

app.use(cors())

app.get('/poke', function (req, res) {
	var pin   = 40;
	var delay = 250;
	var count = 0;
	var max   = 1;

	gpio.setup(pin, gpio.DIR_LOW, on);

	function on() {
		console.log('Welcome to pi');
		
		if (count >= max) {
			gpio.destroy(function() {
				console.log('Closed pins, now exit');
			});
			
			res.send('Done!')
			return;
		}

		console.log('set to 0');
		gpio.write(pin, 0, off);

		count++;
	}

	function off() {
		setTimeout(function() {
			console.log('set to 1');
			gpio.write(pin, 1, on);
		}, delay);
	}
})

app.use('/ui', express.static('page'))

app.listen(3000, function () {
  console.log('App listening on port 3000!')
})
