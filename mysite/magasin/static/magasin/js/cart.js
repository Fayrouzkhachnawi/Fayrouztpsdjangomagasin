document.addEventListener('DOMContentLoaded', function() {
    // Écoutez les clics sur les boutons de suppression
    var deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Empêcher le comportement par défaut du formulaire
            var itemId = this.closest('tr').getAttribute('id').split('-')[1]; // Récupérer l'ID de l'élément
            var itemRow = document.getElementById('item-' + itemId); // Récupérer la ligne correspondante
            if (confirm('Êtes-vous sûr de vouloir supprimer cet élément du panier ?')) {
                itemRow.remove(); // Supprimer la ligne de l'élément du panier
                this.closest('.delete-form').submit(); // Soumettre le formulaire de suppression
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var updateButton = document.getElementById('updateButton');

    updateButton.addEventListener('click', function() {
        updateButton.classList.add('clicked'); // Ajoute la classe 'clicked' au clic
        
        // Supprime la classe 'clicked' après 500ms (ajustez selon vos besoins)
        setTimeout(function() {
            updateButton.classList.remove('clicked');
        }, 500);
    });
});



