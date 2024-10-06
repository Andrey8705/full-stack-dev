const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("Введите число: ", (numberInput) => {
    const number = parseInt(numberInput);
    if (number % 2 === 0) {
        console.log("Четное");
    } else {
        console.log("Нечетное");
    }
    rl.close();
});
