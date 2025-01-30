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
