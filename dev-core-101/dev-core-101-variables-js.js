let a = parseFloat(prompt("Введите первое число:"));
let b = parseFloat(prompt("Введите второе число:"));
if (b === 0) {
    console.log("Вы запомните, друзья, что на ноль делить нельзя!");
} else {
    let product = a * b;
    let quotient = a / b;
    console.log("Произведение: " + product);
    console.log("Частное: " + quotient);
}
console.log("Привет мир!");
