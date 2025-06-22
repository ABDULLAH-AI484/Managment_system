document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.menu-item input[type="checkbox"]');
    const selectedItemsContainer = document.getElementById('selected-items');
    const grandTotalElement = document.getElementById('grand-total');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectedItems();
            calculateTotal();
        });
    });

    function updateSelectedItems() {
        selectedItemsContainer.innerHTML = '';

        document.querySelectorAll('.menu-item input[type="checkbox"]:checked').forEach(checkbox => {
            const itemId = checkbox.id.replace('item-', '');
            const itemName = checkbox.nextElementSibling.nextSibling.textContent.trim();
            const itemPrice = parseFloat(checkbox.closest('.menu-item').querySelector('.item-price').textContent.replace('$', ''));

            const itemElement = document.createElement('div');
            itemElement.className = 'summary-item';
            itemElement.innerHTML = `
                <span>${itemName}</span>
                <span>$${itemPrice.toFixed(2)}</span>
                <span>1</span>
                <span>$${itemPrice.toFixed(2)}</span>
            `;

            selectedItemsContainer.appendChild(itemElement);
        });
    }

    function calculateTotal() {
        let total = 0;

        document.querySelectorAll('.menu-item input[type="checkbox"]:checked').forEach(checkbox => {
            const itemPrice = parseFloat(checkbox.closest('.menu-item').querySelector('.item-price').textContent.replace('$', ''));
            total += itemPrice;
        });

        grandTotalElement.textContent = `$${total.toFixed(2)}`;
    }

    // Add button functionality
    document.querySelector('.add-button').addEventListener('click', function() {
        // Here you would add logic to add new items to the menu
        alert('Add new item functionality would go here');
    });

    // Payment buttons
    document.querySelector('.pay-button').addEventListener('click', function() {
        alert('Payment processing would go here');
    });

    document.querySelector('.balance-button').addEventListener('click', function() {
        alert('Balance calculation would go here');
    });
});