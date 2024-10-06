const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Введите расстояние в километрах: ", (distanceInput) => {
    const distance = parseFloat(distanceInput);

    
    rl.question("Введите скорость в км/ч: ", (speedInput) => {
        const speed = parseFloat(speedInput);

        const time = distance / speed;

        console.log(`Время пути: ${time.toFixed(2)} часов`);

        rl.close();
    });
});
