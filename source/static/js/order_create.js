function addItem() {
    var itemDiv = document.createElement("div");
    itemDiv.classList.add("item");
    itemDiv.innerHTML = `
        <label>Блюдо:</label>
        <input type="text" name="items[]" required>
        <label>Цена:</label>
        <input type="number" name="prices[]" step="0.01" required>
        <label>Количество:</label>
        <input type="number" name="quantities[]" required>
        <button type="button" onclick="removeItem(this)">Удалить блюдо</button>
    `;

    document.getElementById("items").appendChild(itemDiv);
}

function removeItem(button) {
    button.parentElement.remove();
}

document.querySelector('form').addEventListener('submit', function(event) {
        const items = [];
        const prices = [];
        const quantities = [];

        document.querySelectorAll('input[name="items[]"]').forEach(input => items.push(input.value));
        document.querySelectorAll('input[name="prices[]"]').forEach(input => prices.push(input.value));
        document.querySelectorAll('input[name="quantities[]"]').forEach(input => quantities.push(input.value));

        document.getElementById('hidden_items').value = items.join(',');
        document.getElementById('hidden_prices').value = prices.join(',');
        document.getElementById('hidden_quantities').value = quantities.join(',');

        console.log('Items:', items);
        console.log('Prices:', prices);
        console.log('Quantities:', quantities);

        if (items.length === 0 || prices.length === 0 || quantities.length === 0) {
            alert('Пожалуйста, добавьте хотя бы одно блюдо.');
            event.preventDefault();
        }


    });