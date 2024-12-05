const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Введите первое число: ', (inputA) => {
  let a = parseFloat(inputA);

  rl.question('Введите второе число: ', (inputB) => {
    let b = parseFloat(inputB);

    if (b === 0) {
      console.log('Нельзя делить на ноль');
    } else {
      let product = a * b;
      let quotient = a / b;

      console.log('Произведение: ' + product);
      console.log('Частное: ' + quotient);
    }

    console.log("Привет,мир!");

    rl.close();
  });
});
