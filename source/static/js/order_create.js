function addItem() {
    const itemsDiv = document.getElementById('items');
    const itemDiv = document.createElement('div');
    itemDiv.innerHTML = `
        <label>Блюдо:</label>
        <input type="text" name="items[]">
        <label>Цена:</label>
        <input type="number" name="prices[]" step="0.01">
        <label>Количество:</label>
        <input type="number" name="quantities[]">
    `;
    itemsDiv.appendChild(itemDiv);
}

