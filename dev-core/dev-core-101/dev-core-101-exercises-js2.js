const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Введите температуру в градусах Цельсия: ", (celsiusInput) => {
    const celsius = parseFloat(celsiusInput);
    const fahrenheit = (celsius * 9/5) + 32;
    console.log(`Температура в градусах Фаренгейта: ${fahrenheit.toFixed(2)}`);
    rl.close();
});
